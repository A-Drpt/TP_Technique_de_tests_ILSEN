"""Tests API du Triangulator (contrat HTTP)."""

from __future__ import annotations

import pytest


@pytest.fixture
def api_client():
    """Client Flask de test."""
    try:
        from triangulator.app import app
    except ModuleNotFoundError:
        pytest.fail("Module `triangulator.app` absent: API à implémenter.")

    app.config["TESTING"] = True
    return app.test_client()


def test_get_triangulation_uuid_mal_forme_retourne_400(api_client):
    """Un identifiant invalide doit produire une erreur 400."""
    response = api_client.get("/triangulation/not-a-uuid")

    assert response.status_code == 400


def test_get_triangulation_uuid_mal_forme_retourne_objet_erreur(api_client):
    """Le body d'erreur doit contenir `code` et `message`."""
    response = api_client.get("/triangulation/not-a-uuid")
    payload = response.get_json()

    assert isinstance(payload, dict)
    assert "code" in payload
    assert "message" in payload


def test_get_triangulation_uuid_valide_inexistant_retourne_404(api_client):
    """UUID valide mais inconnu -> 404."""
    response = api_client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000")

    assert response.status_code == 404


def test_post_sur_endpoint_get_uniquement_retourne_405(api_client):
    """L'endpoint de triangulation n'accepte pas POST."""
    response = api_client.post("/triangulation/123e4567-e89b-12d3-a456-426614174000")

    assert response.status_code == 405
