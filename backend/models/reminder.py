"""Reminder for returns, maintenance, insurance renewals, etc."""
from datetime import date
from ..extensions import db


class Reminder(db.Model):
    __tablename__ = "reminders"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id  = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    reminder_type = db.Column(db.String(40), nullable=False)  # 'return', 'service', ...
    due_date = db.Column(db.Date, default=date.today)
    sent  = db.Column(db.Boolean, default=False)      # flip true after email/SMS push

    def __repr__(self):
        return f"<Reminder {self.vehicle_id}:{self.reminder_type} @ {self.due_date}>"
