"""Internal star-rating records about clients (helps flag risky renters)."""
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.client_rating import ClientRating
from ..schemas.client_rating_schema import (
    client_rating_schema,
    client_ratings_schema,
)

rating_bp = Blueprint("client_ratings", __name__)


@rating_bp.post("/")
def create_rating():
    rating = client_rating_schema.load(request.get_json())
    db.session.add(rating)
    db.session.commit()
    return client_rating_schema.jsonify(rating), 201


@rating_bp.get("/client/<int:client_id>")
def list_ratings(client_id):
    q = ClientRating.query.filter_by(client_id=client_id).all()
    return client_ratings_schema.jsonify(q), 200


@rating_bp.delete("/<int:rating_id>")
def delete_rating(rating_id):
    rating = ClientRating.query.get_or_404(rating_id)
    db.session.delete(rating)
    db.session.commit()
    return jsonify({"deleted": rating_id}), 204
