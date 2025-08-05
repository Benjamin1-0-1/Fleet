from extensions import db
from datetime import datetime

class VehicleCost(db.Model):
    __tablename__ = 'vehicle_costs'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    type = db.Column(db.String(30))  # purchase, repair, fuel, insurance
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
