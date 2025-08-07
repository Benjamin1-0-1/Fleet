from datetime import datetime
from extensions import db

class VehicleUsageRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id  = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    date_out = db.Column(db.DateTime)
    date_return = db.Column(db.DateTime)
    income = db.Column(db.Float)
