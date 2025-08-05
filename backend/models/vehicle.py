from extensions import db
from datetime import datetime

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(30))
    classification = db.Column(db.String(30))
    costs = db.relationship('VehicleCost', backref='vehicle', lazy=True)
    status_history = db.relationship('VehicleStatusHistory', backref='vehicle', lazy=True)
    usage_records = db.relationship('VehicleUsageRecord', backref='vehicle', lazy=True)
