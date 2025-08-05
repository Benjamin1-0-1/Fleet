from extensions import db
from datetime import datetime

class VehicleUsageRecord(db.Model):
    __tablename__ = 'vehicle_usage_records'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    rented_out = db.Column(db.DateTime, nullable=False)
    returned_at = db.Column(db.DateTime)
    income = db.Column(db.Float, nullable=False)
