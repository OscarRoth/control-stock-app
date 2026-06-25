from datetime import datetime

from flask_login import UserMixin

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


class User(UserMixin):
    ROLE_LABELS = {
        "admin": "Administrador",
        "operador": "Operador",
        "consulta": "Consulta",
    }

    def __init__(self, username, role):
        self.id = username
        self.username = username
        self.role = role

    @property
    def role_label(self):
        return self.ROLE_LABELS.get(self.role, self.role)

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_operador(self):
        return self.role == "operador"

    @property
    def is_consulta(self):
        return self.role == "consulta"

    @property
    def can_manage_products(self):
        return self.role == "admin"

    @property
    def can_move_stock(self):
        return self.role in ("admin", "operador")

    @property
    def can_view_history(self):
        return self.role in ("admin", "consulta")

    @property
    def can_manage_users(self):
        return self.role == "admin"

    @property
    def can_export_products(self):
        return self.role in ("admin", "consulta")