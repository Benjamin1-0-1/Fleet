"""Endpoints to manage reminders."""
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.reminder import Reminder
from ..schemas.reminderSchema import reminder_schema, reminders_schema

reminder_bp = Blueprint("reminders", __name__)


@reminder_bp.post("/")
def create_reminder():
    reminder = reminder_schema.load(request.get_json())
    db.session.add(reminder)
    db.session.commit()
    return reminder_schema.jsonify(reminder), 201


@reminder_bp.get("/")
def list_reminders():
    return reminders_schema.jsonify(Reminder.query.all()), 200


@reminder_bp.patch("/<int:reminder_id>")
def mark_sent(reminder_id):
    reminder = Reminder.query.get_or_404(reminder_id)
    reminder.sent = True
    db.session.commit()
    return reminder_schema.jsonify(reminder), 200
