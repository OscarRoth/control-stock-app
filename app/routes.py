



from datetime import datetime
import csv
from io import StringIO
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    Response
)
from flask_login import login_user, logout_user, login_required, current_user

from . import db
from .models import Product, Movement, User

# permisos para diferentes usuarios
from .permissions import require_role


bp = Blueprint("main", __name__)


def horario_permitido():
    hora = datetime.now().hour
    return 8 <= hora < 18


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not horario_permitido():
            return "Acceso fuera de horario permitido"

        username = request.form["username"]

        #condicionales para tipos de roles para el logueo
        if username == "admin":
            role = "admin"
        elif username == "operador":
            role = "operador"
        else:
            role = "consulta"

        user = User(username=username, role=role)
        session["role"] = role
        login_user(user)

        return redirect(url_for("main.home"))

    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("main.login"))


@bp.route("/")
@login_required
def home():
    products_count = Product.query.count()
    movements_count = Movement.query.count()

    return render_template(
        "base.html",
        content=f"""
        <h2>Inicio</h2>
        <p>Usuario: {current_user.username}</p>
        <p>Rol: {current_user.role}</p>
        <p>Productos registrados: {products_count}</p>
        <p>Movimientos registrados: {movements_count}</p>
        """
    )


@bp.route("/productos")
@login_required
def productos():
    products = Product.query.order_by(Product.name).all()
    return render_template("productos.html", products=products)


@bp.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
@require_role("admin")
def nuevo_producto():
    if request.method == "POST":
        sku = request.form["sku"].strip()
        name = request.form["name"].strip()
        stock = int(request.form["stock"])

        if stock < 0:
            return "Error: el stock inicial no puede ser negativo"

        existing = Product.query.filter_by(sku=sku).first()

        if existing:
            return "Error: ya existe un producto con ese SKU"

        product = Product(sku=sku, name=name, stock=stock)
        db.session.add(product)
        db.session.commit()

        return redirect(url_for("main.productos"))

    return render_template("producto_form.html")


@bp.route("/movimientos", methods=["GET", "POST"])
@login_required
@require_role("admin", "operador")
def movimientos():
    if request.method == "POST":
        product_id = int(request.form["product_id"])


        movement_type = request.form["movement_type"]
        quantity = int(request.form["quantity"])

        if quantity <= 0:
            return "Error: la cantidad debe ser mayor a cero"

        product = Product.query.get(product_id)

        if not product:
            return "Error: producto no encontrado"
        
        if movement_type == "ingreso":
            product.stock += quantity

        elif movement_type == "egreso":
            if product.stock < quantity:
                return "Stock insuficiente"

            product.stock -= quantity

        movement = Movement(
            product_id=product.id,
            movement_type=movement_type,
            quantity=quantity,
            username=current_user.username
        )

        db.session.add(movement)
        db.session.commit()

        return redirect(url_for("main.productos"))

    products = Product.query.order_by(Product.name).all()

    return render_template("movimientos.html", products=products)


@bp.route("/historial")
@login_required
@require_role("admin", "consulta")
def historial():
    movements = Movement.query.order_by(
        Movement.created_at.desc()
    ).all()

    return render_template("historial.html", movements=movements)

@bp.route("/exportar/productos")
@login_required
@require_role("admin", "consulta")
def exportar_productos():

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "SKU",
        "Nombre",
        "Stock"
    ])

    products = Product.query.order_by(Product.id).all()

    for p in products:

        writer.writerow([
            p.id,
            p.sku,
            p.name,
            p.stock
        ])

    csv_data = output.getvalue()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=productos.csv"
        }
    )