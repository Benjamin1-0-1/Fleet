from datetime import datetime
from extensions import db

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id  = db.Column(db.Integer, db.ForeignKey('client.id'))
    filename = db.Column(db.String(200))
    url = db.Column(db.String(300))
    uploaded_at= db.Column(db.DateTime, default=datetime.utcnow)
