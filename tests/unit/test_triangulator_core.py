"""Tests unitaires du coeur du Triangulator (fonction `triangulate`)."""

from __future__ import annotations


def test_moins_de_trois_points_retourne_aucun_triangle(triangulate):
    """Avec moins de 3 points, aucune triangulation n'est possible."""
    assert triangulate([]) == []
    assert triangulate([(0.0, 0.0)]) == []
    assert triangulate([(0.0, 0.0), (1.0, 0.0)]) == []


def test_trois_points_non_colineaires_retourne_un_triangle(triangulate):
    """Trois points non colinéaires doivent former un triangle unique."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    triangles = triangulate(points)

    assert len(triangles) == 1
    assert set(triangles[0]) == {0, 1, 2}


def test_trois_points_colineaires_retourne_aucun_triangle(triangulate):
    """Trois points alignés n'ont pas d'aire, donc pas de triangle."""
    points = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
    triangles = triangulate(points)

    assert triangles == []


def test_quatre_points_en_carre_retourne_deux_triangles(triangulate):
    """Un carré est décomposé en exactement deux triangles."""
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = triangulate(points)

    assert len(triangles) == 2


def test_ajout_point_interieur_divise_un_triangle_en_trois(triangulate):
    """Ajouter un point intérieur à un triangle doit créer 3 sous-triangles."""
    points = [
        (0.0, 0.0),
        (2.0, 0.0),
        (1.0, 2.0),
        (1.0, 0.8),
    ]
    triangles = triangulate(points)

    assert len(triangles) == 3


def test_resultat_est_stable_sur_entrees_identiques(triangulate):
    """Deux appels successifs avec la même entrée gardent le même nombre de triangles."""
    points = [(0.0, 0.0), (2.0, 0.0), (3.0, 1.0), (2.0, 2.0), (0.0, 2.0)]

    triangles_first = triangulate(points)
    triangles_second = triangulate(points)

    assert len(triangles_first) == len(triangles_second)
