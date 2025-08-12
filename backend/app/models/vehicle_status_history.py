from datetime import datetime
from ..extensions import db

class VehicleStatusHistory(db.Model):
    __tablename__ = "vehicle_status_history"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    status = db.Column(db.Enum("in", "out", name="status_enum"), nullable=False, default="out")
    ts_out = db.Column(db.DateTime, default=datetime.utcnow)
    ts_in = db.Column(db.DateTime)

    def __repr__(self):
        return f"<VehicleStatus {self.vehicle_id}:{self.status}>"
