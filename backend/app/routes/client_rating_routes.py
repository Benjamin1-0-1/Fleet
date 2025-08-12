from flask import Blueprint, request
from ..extensions import db
from ..models.client_rating import ClientRating
from ..schemas.client_rating_schema import client_rating_schema, client_ratings_schema

rating_bp = Blueprint("client_ratings", __name__)

@rating_bp.post("/")
def create_rating():
    r = client_rating_schema.load(request.get_json())
    db.session.add(r)
    db.session.commit()
    return client_rating_schema.jsonify(r), 201

@rating_bp.get("/client/<int:client_id>")
def list_ratings(client_id):
    rows = ClientRating.query.filter_by(client_id=client_id).all()
    return client_ratings_schema.jsonify(rows), 200

@rating_bp.delete("/<int:rating_id>")
def delete_rating(rating_id):
    r = ClientRating.query.get_or_404(rating_id)
    db.session.delete(r)
    db.session.commit()
    return {"deleted": rating_id}, 204
