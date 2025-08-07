from datetime import datetime
from extensions import db

class ClientJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id  = db.Column(db.Integer, db.ForeignKey('client.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)
