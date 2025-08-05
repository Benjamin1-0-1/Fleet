from extensions import db
from datetime import datetime

class ClientJob(db.Model):
    __tablename__ = 'client_jobs'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)
    amount = db.Column(db.Float, nullable=False)
