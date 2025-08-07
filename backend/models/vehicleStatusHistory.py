"""Status timeline for a vehicle ─ stores every IN/OUT record.

Why separate table?
• Immutable audit trail (never overwrite the last status).
• Enables utilisation analytics (uptime, downtime, etc.).
"""
from datetime import datetime
from ..extensions import db


class VehicleStatusHistory(db.Model):
    __tablename__ = "vehicle_status_history"

    id   = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)

    # Enum is persisted as text → easy to query / extend later
    status     = db.Column(
        db.Enum("in", "out", name="status_enum"), nullable=False, default="out"
    )
    ts_out = db.Column(db.DateTime, default=datetime.utcnow)  # when left yard
    ts_in  = db.Column(db.DateTime)                           # nullable until returned

    def __repr__(self):
        return f"<VehicleStatus {self.vehicle_id}:{self.status}>"
