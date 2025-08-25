from flask import Blueprint, request, current_app, jsonify
from sqlalchemy import func
from ..extensions import db
from ..models.vehicle import Vehicle
from ..models.vehicle_cost import VehicleCost
from ..models.rental import Rental
from ..models.vehicle_mileage import VehicleMileage
from ..models.damage import Damage
from ..schemas.vehicle_schema import vehicle_schema, vehicles_schema

vehicle_bp = Blueprint("vehicles", __name__)

def _img_url(filename: str | None):
    if not filename: return None
    return f"/static/uploads/{filename}"

@vehicle_bp.post("/")
def create_vehicle():
    vehicle = vehicle_schema.load(request.get_json())
    db.session.add(vehicle)
    db.session.commit()
    return vehicle_schema.jsonify(vehicle), 201

@vehicle_bp.get("/")
def list_vehicles():
    items = Vehicle.query.order_by(Vehicle.id.desc()).all()
    data = vehicles_schema.dump(items)
    for d, v in zip(data, items):
        d["image_url"] = _img_url(v.image_filename)
        # latest mileage
        m = VehicleMileage.query.filter_by(vehicle_id=v.id).order_by(VehicleMileage.recorded_at.desc()).first()
        d["latest_odometer"] = m.odometer if m else None
        # active rental?
        active = Rental.query.filter_by(vehicle_id=v.id, returned_on=None).first()
        d["active_client_id"] = active.client_id if active else None
    return jsonify(data), 200

@vehicle_bp.get("/<int:vehicle_id>")
def get_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    data = vehicle_schema.dump(v)
    data["image_url"] = _img_url(v.image_filename)
    return jsonify(data)

@vehicle_bp.get("/<int:vehicle_id>/detail")
def vehicle_detail(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    # totals
    total_costs = db.session.scalar(db.select(func.coalesce(func.sum(VehicleCost.amount), 0)).filter(VehicleCost.vehicle_id == v.id))
    # revenue from rentals
    rentals = Rental.query.filter_by(vehicle_id=v.id).all()
    total_revenue = 0
    for r in rentals:
        end = r.returned_on or r.end_date or r.start_date
        days = max((end - r.start_date).days + 1, 1)
        total_revenue += float(r.rate_per_day) * days

    # latest mileage
    m = VehicleMileage.query.filter_by(vehicle_id=v.id).order_by(VehicleMileage.recorded_at.desc()).first()
    # damages
    dmg = Damage.query.filter_by(vehicle_id=v.id).order_by(Damage.reported_at.desc()).all()

    return jsonify({
        "vehicle": {
            **vehicle_schema.dump(v),
            "image_url": _img_url(v.image_filename),
            "latest_odometer": (m.odometer if m else None),
        },
        "rentals": [{"id": r.id, "client_id": r.client_id, "start_date": r.start_date.isoformat(),
                     "end_date": (r.end_date.isoformat() if r.end_date else None),
                     "returned_on": (r.returned_on.isoformat() if r.returned_on else None),
                     "rate_per_day": float(r.rate_per_day)} for r in rentals],
        "damages": [{"id": d.id, "description": d.description, "cost": float(d.cost),
                     "reported_at": d.reported_at.isoformat()} for d in dmg],
        "total_costs": float(total_costs or 0),
        "total_revenue": float(total_revenue or 0)
    })
