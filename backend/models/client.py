from extensions import db

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    jobs = db.relationship('ClientJob', backref='client', lazy=True)
    ratings = db.relationship('ClientRating', backref='client', lazy=True)
    contracts = db.relationship('Contract', backref='client', lazy=True)
