from sqlalchemy.orm import backref
from app import db
from os import register_at_fork
from datetime import datetime

class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow())
    rentals = db.relationship('Rental',backref='customer', lazy=True)