"""Tests unitaires sur les propriétés géométriques des triangles générés."""

from __future__ import annotations

from collections import Counter


def _triangle_area2(
    points: list[tuple[float, float]],
    triangle: tuple[int, int, int],
) -> float:
    """Retourne 2x l'aire signée d'un triangle référencé par indices."""
    ax, ay = points[triangle[0]]
    bx, by = points[triangle[1]]
    cx, cy = points[triangle[2]]
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)


def _normalized_edge(i: int, j: int) -> tuple[int, int]:
    """Normalise une arête pour ignorer son orientation."""
    return (i, j) if i < j else (j, i)


def _edge_counter(triangles: list[tuple[int, int, int]]) -> Counter[tuple[int, int]]:
    """Compte le nombre d'occurrences de chaque arête dans les triangles."""
    counter: Counter[tuple[int, int]] = Counter()
    for a, b, c in triangles:
        counter[_normalized_edge(a, b)] += 1
        counter[_normalized_edge(b, c)] += 1
        counter[_normalized_edge(c, a)] += 1
    return counter


def test_points_superposes_ne_creent_pas_de_triangles_degeneres(triangulate):
    """Des points dupliqués ne doivent pas créer de triangles d'aire nulle."""
    points = [
        (0.0, 0.0),
        (1.0, 0.0),
        (0.0, 1.0),
        (0.0, 1.0),
    ]
    triangles = triangulate(points)

    assert all(len(set(triangle)) == 3 for triangle in triangles)
    assert all(_triangle_area2(points, triangle) != 0 for triangle in triangles)


def test_aucune_arete_partagee_par_plus_de_deux_triangles(triangulate):
    """En 2D, une arête ne peut appartenir qu'à 1 ou 2 triangles."""
    points = [
        (0.0, 0.0),
        (2.0, 0.0),
        (3.0, 1.0),
        (2.0, 2.0),
        (0.0, 2.0),
        (-1.0, 1.0),
        (1.0, 1.0),
    ]
    triangles = triangulate(points)
    edge_count = _edge_counter(triangles)

    assert all(count <= 2 for count in edge_count.values())


def test_plusieurs_triangles_autour_d_un_point_pivot(triangulate):
    """Un point central doit être relié à plusieurs triangles en éventail."""
    points = [
        (0.0, 0.0),
        (1.0, 0.0),
        (0.7, 0.7),
        (0.0, 1.0),
        (-0.7, 0.7),
        (-1.0, 0.0),
        (-0.7, -0.7),
        (0.0, -1.0),
        (0.7, -0.7),
    ]
    triangles = triangulate(points)

    triangles_avec_pivot = [t for t in triangles if 0 in t]
    assert len(triangles_avec_pivot) >= 4


def test_triangle_retourne_ne_contient_pas_de_sommet_duplique(triangulate):
    """Un triangle valide doit avoir 3 indices distincts."""
    points = [(0.0, 0.0), (1.5, 0.0), (0.2, 1.2), (1.0, 1.0)]
    triangles = triangulate(points)

    assert all(len(set(triangle)) == 3 for triangle in triangles)


def test_indices_de_triangles_restent_dans_les_bornes(triangulate):
    """Tous les indices renvoyés doivent référencer un point existant."""
    points = [(-1.0, -1.0), (2.0, -1.0), (2.0, 2.0), (-1.0, 2.0), (0.5, 0.5)]
    triangles = triangulate(points)

    assert all(0 <= idx < len(points) for triangle in triangles for idx in triangle)
