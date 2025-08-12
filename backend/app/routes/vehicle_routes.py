from flask import Blueprint, request
from ..extensions import db
from ..models.vehicle import Vehicle
from ..schemas.vehicle_schema import vehicle_schema, vehicles_schema

vehicle_bp = Blueprint("vehicles", __name__)

@vehicle_bp.post("/")
def create_vehicle():
    vehicle = vehicle_schema.load(request.get_json())
    db.session.add(vehicle)
    db.session.commit()
    return vehicle_schema.jsonify(vehicle), 201

@vehicle_bp.get("/")
def list_vehicles():
    return vehicles_schema.jsonify(Vehicle.query.order_by(Vehicle.id.desc()).all()), 200

@vehicle_bp.get("/<int:vehicle_id>")
def get_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    return vehicle_schema.jsonify(v)

@vehicle_bp.patch("/<int:vehicle_id>")
def update_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    for k, val in request.get_json().items():
        setattr(v, k, val)
    db.session.commit()
    return vehicle_schema.jsonify(v)

@vehicle_bp.delete("/<int:vehicle_id>")
def delete_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(v)
    db.session.commit()
    return {"deleted": vehicle_id}, 204
