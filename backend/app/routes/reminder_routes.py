from flask import Blueprint, request
from ..extensions import db
from ..models.reminder import Reminder
from ..schemas.reminder_schema import reminder_schema, reminders_schema
from datetime import date, timedelta
from ..models.rental import Rental
from ..models.vehicle_cost import VehicleCost
from sqlalchemy import and_

reminder_bp = Blueprint("reminders", __name__)

@reminder_bp.post("/")
def create_reminder():
    r = reminder_schema.load(request.get_json())
    db.session.add(r)
    db.session.commit()
    return reminder_schema.jsonify(r), 201

@reminder_bp.get("/")
def list_reminders():
    return reminders_schema.jsonify(Reminder.query.order_by(Reminder.due_date.asc()).all()), 200

@reminder_bp.patch("/<int:reminder_id>")
def update_reminder(reminder_id):
    r = Reminder.query.get_or_404(reminder_id)
    for k, v in request.get_json().items():
        setattr(r, k, v)
    db.session.commit()
    return reminder_schema.jsonify(r), 200

@reminder_bp.delete("/<int:reminder_id>")
def delete_reminder(reminder_id):
    r = Reminder.query.get_or_404(reminder_id)
    db.session.delete(r)
    db.session.commit()
    return {"deleted": reminder_id}, 204

@reminder_bp.get("/all")
def all_reminders():
    saved = reminders_schema.dump(Reminder.query.order_by(Reminder.due_date.asc()).all())
    # overdue rentals (not returned and end_date in past)
    today = date.today()
    overdue = []
    for r in Rental.query.filter(Rental.end_date.isnot(None), Rental.returned_on.is_(None), Rental.end_date < today).all():
        overdue.append({
            "id": f"overdue-{r.id}",
            "vehicle_id": r.vehicle_id,
            "reminder_type": "overdue",
            "due_date": r.end_date.isoformat(),
            "sent": False
        })
        fuel_need = []
        cutoff = today - timedelta(days=14)
        vehicle_ids = {v.id for v in Vehicle.query.all()}
        fueled_ids = {vc.vehicle_id for vc in VehicleCost.query.filter(and_(VehicleCost.cost_type=="fuel", VehicleCost.cost_date >= cutoff)).all()}
        for vid in (vehicle_ids - fueled_ids):
            fuel_need.append({"id": f"fuel-{vid}", "vehicle_id": vid, "reminder_type": "fuel", "due_date": today.isoformat(), "sent": False})

            return jsonify({"saved": saved, "generated": {"overdue": overdue, "fuel": fuel_need}}), 200
