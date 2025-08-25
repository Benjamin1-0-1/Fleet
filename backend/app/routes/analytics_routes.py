from flask import Blueprint, jsonify, request
from datetime import date, timedelta
from sqlalchemy import func
from ..extensions import db
from ..models.vehicle import Vehicle
from ..models.vehicle_cost import VehicleCost
from ..models.rental import Rental

analytics_bp = Blueprint("analytics", __name__)

def _revenue_between(start: date, end: date):
    rentals = Rental.query.filter(Rental.start_date <= end, (Rental.returned_on.is_(None)) | (Rental.returned_on >= start)).all()
    total = 0.0
    for r in rentals:
        r_start = max(r.start_date, start)
        r_end = min((r.returned_on or r.end_date or end), end)
        days = max((r_end - r_start).days + 1, 0)
        total += float(r.rate_per_day) * days
    return total

@analytics_bp.get("/summary")
def summary():
    today = date.today()
    start_week = today - timedelta(days=today.weekday())
    start_month = today.replace(day=1)
    start_year = today.replace(month=1, day=1)

    vehicle_count = db.session.scalar(db.select(func.count()).select_from(Vehicle))
    total_costs = float(db.session.scalar(db.select(func.coalesce(func.sum(VehicleCost.amount), 0))) or 0)

    data = {
        "vehicles": int(vehicle_count or 0),
        "total_costs": total_costs,
        "revenue_week": _revenue_between(start_week, today),
        "revenue_month": _revenue_between(start_month, today),
        "revenue_year": _revenue_between(start_year, today),
    }
    return jsonify(data)
