"""VERY basic analytics stub – expand later with real SQL / Pandas."""
from flask import Blueprint, jsonify
from sqlalchemy import func
from ..extensions import db
from ..models.vehicleCost import VehicleCost
from ..models.vehicle import Vehicle

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.get("/summary")
def summary():
    # total vehicles + aggregate cost so far
    vehicle_count = db.session.scalar(db.select(func.count()).select_from(Vehicle))
    total_costs   = db.session.scalar(
        db.select(func.coalesce(func.sum(VehicleCost.amount), 0))
    )
    return jsonify({"vehicles": vehicle_count, "total_costs": float(total_costs)}), 200
