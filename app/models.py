from datetime import datetime
from . import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    active = db.Column(db.Boolean, nullable=False, default=True)

    movements = db.relationship("Movement", backref="product", lazy=True)


class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    movement_type = db.Column(db.String(10), nullable=False)  # ingreso / egreso
    quantity = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# se crea modelo usr (para conectar a Active Directory)
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.username = username
        self.role = role
    