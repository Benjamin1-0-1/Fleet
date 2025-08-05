from extensions import db
from datetime import datetime

class VehicleStatusHistory(db.Model):
    __tablename__ = 'vehicle_status_history'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'in' or 'out'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
