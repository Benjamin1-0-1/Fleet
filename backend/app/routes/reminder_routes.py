from flask import Blueprint, request
from ..extensions import db
from ..models.reminder import Reminder
from ..schemas.reminder_schema import reminder_schema, reminders_schema

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
