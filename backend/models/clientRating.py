from extensions import db
from datetime import datetime

class ClientRating(db.Model):
    __tablename__ = 'client_ratings'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    rating = db.Column(db.Integer)  # 1 to 5
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
