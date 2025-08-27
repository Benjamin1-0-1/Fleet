from flask import Blueprint, request
from ..extensions import db
from ..models.client import Client
from ..schemas.client_schema import client_schema, clients_schema
from ..models.rental import Rental
from datetime import date

client_bp = Blueprint("clients", __name__)

@client_bp.post("/")
def create_client():
    data = request.get_json() or {}
    c = Client(
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),
        email=data.get("email", ""),
        phone=data.get("phone"),
        address=data.get("address"),
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({"id": c.id}), 201

@client_bp.get("/")
def list_clients():
    clients = Client.query.order_by(Client.id.desc()).all()
    data = [{
        "id": c.id,
        "first_name": c.first_name,
        "last_name": c.last_name,
        "email": c.email,
        "phone": getattr(c, "phone", None),
        "address": getattr(c, "address", None),
    } for c in clients]
    return jsonify(data), 200

@client_bp.get("/<int:client_id>")
def get_client(client_id):
    c = Client.query.get_or_404(client_id)
    return jsonify({
        "id": c.id,
        "first_name": c.first_name,
        "last_name": c.last_name,
        "email": c.email,
        "phone": getattr(c, "phone", None),
        "address": getattr(c, "address", None),
    })

@client_bp.patch("/<int:client_id>")
def update_client(client_id):
    c = Client.query.get_or_404(client_id)
    data = request.get_json() or {}
    for k in ["first_name", "last_name", "email", "phone", "address"]:
        if k in data:
            setattr(c, k, data[k])
    db.session.commit()
    return jsonify({"ok": True}), 200

@client_bp.delete("/<int:client_id>")
def delete_client(client_id):
    c = Client.query.get_or_404(client_id)
    db.session.delete(c)
    db.session.commit()
    return {"deleted": client_id}, 204

@client_bp.get("/summary")
def clients_summary():
    out = []
    clients = Client.query.order_by(Client.id.asc()).all()
    for c in clients:
        # active rental: returned_on is NULL
        active = Rental.query.filter_by(client_id=c.id, returned_on=None).first()
        status = "With Vehicle" if active else "Idle"
        days = (date.today() - active.rented_on).days if active and active.rented_on else 0
        out.append({
            "id": c.id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "email": c.email,
            "phone": getattr(c, "phone", None),
            "status": status,
            "current_vehicle_id": active.vehicle_id if active else None,
            "days_with_vehicle": days,
        })
    return jsonify(out), 200
