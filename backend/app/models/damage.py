from datetime import datetime
from ..extensions import db

class Damage(db.Model):
    __tablename__ = "damages"
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Numeric(10, 2), default=0)
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)

    vehicle = db.relationship("Vehicle", backref=db.backref("damages", cascade="all,delete"))
