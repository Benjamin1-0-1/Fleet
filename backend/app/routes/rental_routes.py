from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.rental import Rental
from ..schemas.rental_schema import rental_schema, rentals_schema

rental_bp = Blueprint("rentals", __name__)

@rental_bp.get("/")
def list_rentals():
    return rentals_schema.jsonify(Rental.query.order_by(Rental.id.desc()).all())

@rental_bp.post("/")
@jwt_required()
def create_rental():
    r = rental_schema.load(request.get_json())
    db.session.add(r)
    db.session.commit()
    return rental_schema.jsonify(r), 201

@rental_bp.patch("/<int:rental_id>")
@jwt_required()
def update_rental(rental_id):
    r = Rental.query.get_or_404(rental_id)
    for k, v in (request.get_json() or {}).items():
        setattr(r, k, v)
    db.session.commit()
    return rental_schema.jsonify(r)

@rental_bp.delete("/<int:rental_id>")
@jwt_required()
def delete_rental(rental_id):
    r = Rental.query.get_or_404(rental_id)
    db.session.delete(r)
    db.session.commit()
    return {"deleted": rental_id}, 204
