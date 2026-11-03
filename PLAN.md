# TODO

# Tests Workflow & Intégration

| Cas | Action effectuée | Résultat attendu | Justification (Pourquoi on fait ça) |
| :--- | :--- | :--- | :--- |
| **Envoi du PointSet au PointSetManager** | Le Client envoie un ensemble de points via une requête HTTP POST au `PointSetManager`. | Le `PointSetManager` répond avec un code de succès (ex. 200/201) et un identifiant `PSID`. | S'assurer que le système accepte et comprend bien la demande initiale d'enregistrement envoyée par l'utilisateur. |
| **Persistance BDD & Attribution du PSID** | Le `PointSetManager` reçoit les points, les stocke en base et génère le `PSID`. | Les points sont bien enregistrés en base et le `PSID` permet de les retrouver sans erreur. | Vérifier que les données ne sont ni perdues ni modifiées pendant la sauvegarde pour pouvoir les réutiliser plus tard. |
| **Validation du PSID par le Triangulator** | Le Client demande un calcul au `Triangulator` avec un `PSID` erroné, puis avec un `PSID` valide. | Erreur (404/400) si l'identifiant n'existe pas ; requête acceptée s'il est correct. | Éviter que le serveur ne tente de travailler sur des données inexistantes ou ne plante face à un mauvais identifiant. |
| **Récupération du PointSet par le Triangulator** | Le `Triangulator` demande les données au `PointSetManager` avec le `PSID`. | Le `PointSetManager` renvoie les points exacts et le `Triangulator` les lit correctement. | Vérifier que les deux serveurs communiquent bien ensemble et s'échangent les données sans les déformer. |
| **Workflow complet & Réponse Client** | Le Client lance une demande complète avec un `PSID` existant. | Le `Triangulator` calcule et renvoie la liste des triangles attendus au Client. | Confirmer que toute la chaîne fonctionne du début à la fin du point de vue de l'utilisateur. |

# Tests Unitaires (Algorithme géométrique)

| Cas | Action effectuée | Résultat attendu | Justification (Pourquoi on fait ça) |
| :--- | :--- | :--- | :--- |
| **Moins de 3 points** (0, 1 ou 2 points) | Donner 0, 1 ou 2 points au moteur de calcul. | 0 triangle renvoyé ou erreur explicite gérée proprement. | Un triangle nécessite au minimum 3 sommets ; il faut vérifier que le programme ne plante pas face à une saisie incomplète. |
| **Plus de 3 points** (Cas standard, ex. 4 ou 5 points) | Donner un ensemble classique de points bien répartis. | Des triangles valides qui couvrent tous les points sans se superposer ni laisser de trous. | Valider le fonctionnement normal du calcul sur un exemple simple de référence. |
| **Points superposés** (ex. 4 points dont 2 avec les mêmes coordonnées) | Donner des points situés exactement au même endroit. | Les doublons sont fusionnés ou ignorés sans faire planter le calcul. | Deux points identiques créent des figures invisibles ou « plates » qui peuvent fausser les calculs ou provoquer des divisions par zéro. |
| **Points alignés** (ex. 3 points sur une même ligne) | Donner 3 points situés sur une même droite. | 0 triangle renvoyé (ou cas géré proprement). | Des points en ligne droite forment un trait et non un triangle ; le programme doit reconnaître qu'aucune surface ne peut être créée. |
| **Deux triangles avec un côté commun** | Donner 4 points formant une surface simple (ex. un carré). | Exactement 2 triangles collés par une arête commune. | Contrôler que l'algorithme sait assembler deux triangles voisins sans les faire se chevaucher. |
| **Plus de deux triangles sur une même arête** | Tester une configuration où une arête pourrait être partagée par 3 faces ou plus. | Une arête n'est partagée que par 2 triangles au maximum. | Sur un plan en 2D, deux faces ne peuvent pas se replier l'une sur l'autre ; cela garantit un tracé net et à plat. |
| **Plusieurs triangles autour d'un point pivot** | Placer un point central entouré de plusieurs points en cercle. | Des triangles organisés en éventail qui se rejoignent tous au centre. | Vérifier que l'algorithme gère bien un carrefour où beaucoup de triangles se rejoignent sur un seul sommet. |
| **Ajout de points dans un triangle existant** | Ajouter un point au milieu d'un triangle, puis recommencer dans les sous-triangles. | Le triangle d'origine se divise proprement en 3 nouveaux triangles à chaque ajout. | Vérifier comment le programme découpe progressivement l'espace et s'il supporte des niveaux de détail successifs sans saturer. |