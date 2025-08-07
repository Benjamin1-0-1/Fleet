"""Optional star-rating left by the business about a client."""
from datetime import date
from ..extensions import db


class ClientRating(db.Model):
    __tablename__ = "client_ratings"

    id    = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    stars = db.Column(db.Integer, nullable=False)  # 1-5
    feedback  = db.Column(db.Text)
    rated_on  = db.Column(db.Date, default=date.today)

    def __repr__(self):
        return f"<Rating {self.client_id}:{self.stars}★>"
