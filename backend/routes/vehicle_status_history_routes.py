"""Read-only history of every IN / OUT entry for audit + utilisation stats."""
from flask import Blueprint
from ..models.vehicle_status_history import VehicleStatusHistory
from ..schemas.vehicle_status_history_schema import (
    vehicle_status_history_schemas,
)

status_bp = Blueprint("vehicle_status_history", __name__)


@status_bp.get("/vehicle/<int:vehicle_id>")
def history_for_vehicle(vehicle_id):
    q = VehicleStatusHistory.query.filter_by(vehicle_id=vehicle_id).all()
    return vehicle_status_history_schemas.jsonify(q), 200
