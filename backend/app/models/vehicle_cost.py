from datetime import date
from ..extensions import db

class VehicleCost(db.Model):
    __tablename__ = "vehicle_costs"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    cost_type = db.Column(db.Enum("repair", "fuel", "insurance", name="cost_type_enum"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    cost_date = db.Column(db.Date, default=date.today)
    remark = db.Column(db.Text)

    def __repr__(self):
        return f"<Cost {self.vehicle_id}:{self.cost_type} {self.amount}>"
