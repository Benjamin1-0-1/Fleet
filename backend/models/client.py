"""Customer / renter of vehicles."""
from datetime import datetime
from ..extensions import db


class Client(db.Model):
    __tablename__ = "clients"

    id  = db.Column(db.Integer, primary_key=True)
    first_name  = db.Column(db.String(40), nullable=False)
    last_name   = db.Column(db.String(40), nullable=False)
    phone  = db.Column(db.String(20))
    email  = db.Column(db.String(80), unique=True)
    address  = db.Column(db.String(120))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    ratings = db.relationship("ClientRating", backref="client", lazy=True)

    def __repr__(self):
        return f"<Client {self.first_name} {self.last_name}>"
