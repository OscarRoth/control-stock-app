from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

#importar login  (para conectar a Active Directory)
from flask_login import LoginManager

from flask import Flask, session

db = SQLAlchemy()

# (para conectar a Active Directory)
login_manager = LoginManager()
login_manager.login_view = "main.login"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from . import models

    with app.app_context():
        db.create_all()

    from .routes import bp
    app.register_blueprint(bp)

    return app


from .models import User

@login_manager.user_loader
def load_user(user_id):
    role = session.get("role", "consulta")
    return User(user_id, role)