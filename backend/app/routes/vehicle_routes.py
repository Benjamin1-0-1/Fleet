from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models.vehicle import Vehicle

vehicle_bp = Blueprint("vehicles", __name__)

@vehicle_bp.get("/")
def list_vehicles():
    rows = Vehicle.query.order_by(Vehicle.id.desc()).all()
    return jsonify([{
        "id": v.id, "plate": v.plate, "make": v.make, "model": v.model,
        "v_class": getattr(v, "v_class", None),
        "colour": getattr(v, "colour", None),
        "purchase_price": getattr(v, "purchase_price", None),
    } for v in rows]), 200

@vehicle_bp.post("/")
def create_vehicle():
    d = request.get_json() or {}
    v = Vehicle(
        plate=d.get("plate",""),
        make=d.get("make",""),
        model=d.get("model",""),
        v_class=d.get("v_class"),
        colour=d.get("colour"),
        purchase_price=d.get("purchase_price"),
    )
    db.session.add(v); db.session.commit()
    return jsonify({"id": v.id}), 201

@vehicle_bp.get("/<int:vehicle_id>")
def get_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    return jsonify({
        "id": v.id, "plate": v.plate, "make": v.make, "model": v.model,
        "v_class": getattr(v, "v_class", None),
        "colour": getattr(v, "colour", None),
        "purchase_price": getattr(v, "purchase_price", None),
    }), 200

@vehicle_bp.patch("/<int:vehicle_id>")
def update_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    d = request.get_json() or {}
    for k in ["plate","make","model","v_class","colour","purchase_price"]:
        if k in d: setattr(v, k, d[k])
    db.session.commit()
    return jsonify({"ok": True}), 200
