from flask import Blueprint, request
from ..extensions import db
from ..models.client import Client
from ..schemas.client_schema import client_schema, clients_schema

client_bp = Blueprint("clients", __name__)

@client_bp.post("/")
def create_client():
    client = client_schema.load(request.get_json())
    db.session.add(client)
    db.session.commit()
    return client_schema.jsonify(client), 201

@client_bp.get("/")
def list_clients():
    return clients_schema.jsonify(Client.query.order_by(Client.id.desc()).all()), 200

@client_bp.get("/<int:client_id>")
def get_client(client_id):
    c = Client.query.get_or_404(client_id)
    return client_schema.jsonify(c)

@client_bp.patch("/<int:client_id>")
def update_client(client_id):
    c = Client.query.get_or_404(client_id)
    for k, v in request.get_json().items():
        setattr(c, k, v)
    db.session.commit()
    return client_schema.jsonify(c)

@client_bp.delete("/<int:client_id>")
def delete_client(client_id):
    c = Client.query.get_or_404(client_id)
    db.session.delete(c)
    db.session.commit()
    return {"deleted": client_id}, 204
