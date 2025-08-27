from datetime import date, datetime
from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models.reminder import Reminder
from ..models.rental import Rental
from ..models.vehicle import Vehicle

reminder_bp = Blueprint("reminders", __name__)


def _parse_due(val):
    """Accept date or ISO string; return date or None."""
    if not val:
        return None
    if isinstance(val, date):
        return val
    try:
        # try full ISO datetime first, then date
        return datetime.fromisoformat(val).date()
    except Exception:
        try:
            return datetime.strptime(val, "%Y-%m-%d").date()
        except Exception:
            return None


@reminder_bp.post("/")
def create_reminder():
    data = request.get_json() or {}
    r = Reminder(
        vehicle_id=data.get("vehicle_id"),
        reminder_type=data.get("reminder_type", "general"),
        due_date=_parse_due(data.get("due_date")),
        notes=data.get("notes"),
    )
    db.session.add(r)
    db.session.commit()
    return jsonify({"id": r.id}), 201


@reminder_bp.get("/")
def list_reminders():
    items = Reminder.query.order_by(Reminder.due_date.asc().nulls_last()).all()
    out = [{
        "id": r.id,
        "vehicle_id": r.vehicle_id,
        "reminder_type": r.reminder_type,
        "due_date": r.due_date.isoformat() if r.due_date else None,
        "notes": getattr(r, "notes", None),
    } for r in items]
    return jsonify(out), 200


@reminder_bp.patch("/<int:reminder_id>")
def update_reminder(reminder_id):
    r = Reminder.query.get_or_404(reminder_id)
    data = request.get_json() or {}
    if "vehicle_id" in data:
        r.vehicle_id = data["vehicle_id"]
    if "reminder_type" in data:
        r.reminder_type = data["reminder_type"]
    if "due_date" in data:
        r.due_date = _parse_due(data["due_date"])
    if "notes" in data:
        r.notes = data["notes"]
    db.session.commit()
    return jsonify({
        "id": r.id,
        "vehicle_id": r.vehicle_id,
        "reminder_type": r.reminder_type,
        "due_date": r.due_date.isoformat() if r.due_date else None,
        "notes": getattr(r, "notes", None),
    }), 200


@reminder_bp.delete("/<int:reminder_id>")
def delete_reminder(reminder_id):
    r = Reminder.query.get_or_404(reminder_id)
    db.session.delete(r)
    db.session.commit()
    # use 200 with a body (204 should not return a body)
    return jsonify({"deleted": reminder_id}), 200


@reminder_bp.get("/all")
def reminders_all():
    """Combined feed: saved reminders + generated (overdue rentals, low fuel)."""
    # saved reminders
    saved = Reminder.query.order_by(Reminder.due_date.asc().nulls_last()).all()
    saved_out = [{
        "id": r.id,
        "vehicle_id": r.vehicle_id,
        "reminder_type": r.reminder_type,
        "due_date": r.due_date.isoformat() if r.due_date else None,
        "notes": getattr(r, "notes", None),
    } for r in saved]

    # generated: overdue rentals
    overdue_out = []
    today = date.today()
    active = Rental.query.filter(Rental.returned_on.is_(None)).all()
    for rr in active:
        due_on = getattr(rr, "due_on", None)
        if due_on and isinstance(due_on, date) and due_on < today:
            overdue_out.append({
                "vehicle_id": rr.vehicle_id,
                "reminder_type": "overdue_rental",
                "due_date": due_on.isoformat(),
                "client_id": rr.client_id,
            })

    # generated: low fuel (if model has fuel_level)
    fuel_out = []
    for v in Vehicle.query.all():
        fuel = getattr(v, "fuel_level", None)
        try:
            if fuel is not None and float(fuel) <= 15:
                fuel_out.append({
                    "vehicle_id": v.id,
                    "reminder_type": "fuel_low",
                    "level": float(fuel),
                    "due_date": None,
                })
        except Exception:
            pass

    # return in the shape the frontend expects,
    # but also include the flat keys for compatibility.
    payload = {
        "saved": saved_out,
        "generated": {"overdue": overdue_out, "fuel": fuel_out},
        "overdue_rentals": overdue_out,
        "fuel_needed": fuel_out,
    }
    return jsonify(payload), 200
