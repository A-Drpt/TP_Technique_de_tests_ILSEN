"""API Flask du Triangulator (squelette minimal)."""

from __future__ import annotations

from uuid import UUID

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/triangulation/<point_set_id>")
def get_triangulation(point_set_id: str):
    """Endpoint minimal pour valider le contrat HTTP de base."""
    try:
        UUID(point_set_id)
    except ValueError:
        return jsonify({"code": "INVALID_POINTSET_ID", "message": "Invalid PointSetID format."}), 400

    return jsonify({"code": "NOT_FOUND", "message": "PointSet not found."}), 404
