from datetime import date
from ..extensions import db

class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=date.today)
    end_date = db.Column(db.Date)  # planned end
    returned_on = db.Column(db.Date)  # actual return (null if active)
    rate_per_day = db.Column(db.Numeric(10, 2), nullable=False)

    vehicle = db.relationship("Vehicle", backref=db.backref("rentals", cascade="all,delete"))
