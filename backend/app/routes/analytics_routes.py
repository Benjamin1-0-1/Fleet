from flask import Blueprint, jsonify
from sqlalchemy import func
from ..extensions import db
from ..models.vehicle import Vehicle
# Rentals / Damages may or may not have these columns in your DB; handle gracefully.
try:
    from ..models.rental import Rental  # optional
except Exception:
    Rental = None
try:
    from ..models.damage import Damage  # optional
except Exception:
    Damage = None

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.get("/summary")
def summary():
    vehicles = db.session.query(func.count(Vehicle.id)).scalar() or 0

    # total maintenance costs (safe if Damage model/column missing)
    total_costs = 0.0
    if Damage is not None and hasattr(Damage, "cost"):
        total_costs = float(db.session.query(func.coalesce(func.sum(Damage.cost), 0)).scalar() or 0)

    # revenue (safe if Rental model/column missing)
    revenue_year = 0.0
    if Rental is not None:
        # prefer 'amount' then 'total' then 0
        if hasattr(Rental, "amount"):
            revenue_year = float(db.session.query(func.coalesce(func.sum(Rental.amount), 0)).scalar() or 0)
        elif hasattr(Rental, "total"):
            revenue_year = float(db.session.query(func.coalesce(func.sum(Rental.total), 0)).scalar() or 0)
        else:
            revenue_year = 0.0

    # simple placeholders if you don't track by month/week yet
    revenue_month = revenue_year
    revenue_week = 0.0

    return jsonify({
        "vehicles": vehicles,
        "total_costs": total_costs,
        "revenue_year": revenue_year,
        "revenue_month": revenue_month,
        "revenue_week": revenue_week,
    }), 200
