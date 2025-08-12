from datetime import date
from ..extensions import db

class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    colour = db.Column(db.String(30))
    v_class = db.Column(db.String(30))
    purchase_price = db.Column(db.Numeric(10, 2))
    purchase_date = db.Column(db.Date, default=date.today)
    expected_resale = db.Column(db.Numeric(10, 2))

    costs = db.relationship("VehicleCost", backref="vehicle", lazy=True, cascade="all,delete")
    statuses = db.relationship("VehicleStatusHistory", backref="vehicle", lazy=True, cascade="all,delete")
    reminders = db.relationship("Reminder", backref="vehicle", lazy=True, cascade="all,delete")

    def __repr__(self):
        return f"<Vehicle {self.plate}>"
