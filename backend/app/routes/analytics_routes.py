from flask import Blueprint, jsonify
from sqlalchemy import func
from ..extensions import db
from ..models.vehicle import Vehicle
from ..models.vehicle_cost import VehicleCost

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.get("/summary")
def summary():
    vehicle_count = db.session.scalar(db.select(func.count()).select_from(Vehicle))
    total_costs = db.session.scalar(db.select(func.coalesce(func.sum(VehicleCost.amount), 0)))
    return jsonify({"vehicles": int(vehicle_count or 0), "total_costs": float(total_costs or 0.0)})
