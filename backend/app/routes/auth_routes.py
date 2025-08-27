from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(username=data.get("username", "")).first()
    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"msg": "Bad credentials"}), 401
    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200
