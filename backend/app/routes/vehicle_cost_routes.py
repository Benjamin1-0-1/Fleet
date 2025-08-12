from flask import Blueprint, request
from ..extensions import db
from ..models.vehicle_cost import VehicleCost
from ..schemas.vehicle_cost_schema import vehicle_cost_schema, vehicle_costs_schema

vehicle_cost_bp = Blueprint("vehicle_costs", __name__)

@vehicle_cost_bp.post("/")
def create_cost():
    cost = vehicle_cost_schema.load(request.get_json())
    db.session.add(cost)
    db.session.commit()
    return vehicle_cost_schema.jsonify(cost), 201

@vehicle_cost_bp.get("/")
def list_costs():
    return vehicle_costs_schema.jsonify(VehicleCost.query.all()), 200

@vehicle_cost_bp.patch("/<int:cost_id>")
def update_cost(cost_id):
    cost = VehicleCost.query.get_or_404(cost_id)
    for k, v in request.get_json().items():
        setattr(cost, k, v)
    db.session.commit()
    return vehicle_cost_schema.jsonify(cost), 200

@vehicle_cost_bp.delete("/<int:cost_id>")
def delete_cost(cost_id):
    cost = VehicleCost.query.get_or_404(cost_id)
    db.session.delete(cost)
    db.session.commit()
    return {"deleted": cost_id}, 204
