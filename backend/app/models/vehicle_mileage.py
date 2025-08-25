from datetime import datetime
from ..extensions import db

class VehicleMileage(db.Model):
    __tablename__ = "vehicle_mileage"
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    odometer = db.Column(db.Integer, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    vehicle = db.relationship("Vehicle", backref=db.backref("mileage_logs", cascade="all,delete"))
