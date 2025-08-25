from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models.user import User
from ..extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    u = User.query.filter_by(username=data.get("username")).first()
    if not u or not u.check_password(data.get("password") or ""):
        return jsonify({"msg": "Bad credentials"}), 401
    token = create_access_token(identity=u.id)
    return jsonify({"access_token": token})
