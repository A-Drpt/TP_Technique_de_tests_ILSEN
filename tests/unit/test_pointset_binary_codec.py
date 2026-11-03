"""Tests unitaires du codec binaire des `PointSet`.

Convention cible (test-first):
- module: `triangulator.codec`
- fonctions: `encode_pointset(points)` et `decode_pointset(raw)`
"""

from __future__ import annotations

import pytest


@pytest.fixture
def pointset_codec():
    """Charge les fonctions d'encodage/décodage du PointSet."""
    try:
        from triangulator.codec import decode_pointset, encode_pointset
    except ModuleNotFoundError:
        pytest.fail("Module `triangulator.codec` absent: codec binaire à implémenter.")
    except ImportError:
        pytest.fail(
            "Fonctions `encode_pointset`/`decode_pointset` absentes dans `triangulator.codec`."
        )

    return encode_pointset, decode_pointset


def test_pointset_encode_decode_roundtrip(pointset_codec):
    """Un PointSet encodé puis décodé doit retrouver les mêmes points."""
    encode_pointset, decode_pointset = pointset_codec
    points = [(0.0, 0.0), (1.5, -2.0), (3.25, 4.75)]

    payload = encode_pointset(points)
    decoded_points = decode_pointset(payload)

    assert decoded_points == points


def test_pointset_vide_roundtrip(pointset_codec):
    """Le PointSet vide doit être supporté."""
    encode_pointset, decode_pointset = pointset_codec

    payload = encode_pointset([])
    decoded_points = decode_pointset(payload)

    assert decoded_points == []


def test_decode_pointset_rejette_payload_tronque(pointset_codec):
    """Un payload incomplet doit déclencher une erreur explicite."""
    _, decode_pointset = pointset_codec
    payload_tronque = b"\x01\x00\x00\x00\x00\x00\x00"

    with pytest.raises(ValueError):
        decode_pointset(payload_tronque)
