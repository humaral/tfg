# Autor: Hugo Martín Alonso
# Descripción: programa de inicialización de la aplicación.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_login import LoginManager
from flask_mail import Mail, Message
from .config import Config
from datetime import datetime


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    #Se establecen variables globales en las plantillas que se actualizan al refrescar la página
    @app.context_processor
    def inject_globals():
        return {
            "current_date": datetime.now().strftime('%d/%m/%Y'),
            "current_year": datetime.now().year
        }
    
    if app.config['REINICIAR_BD_ON_STARTUP']:
        from .utils import reiniciar_bd
        reiniciar_bd(app)

    from app import models

    @login_manager.user_loader
    def load_user(idEmpleado):
        stmt = select(models.Empleado).where(models.Empleado.id == int(idEmpleado))
        user = db.session.scalar(stmt)
        return user if user and user.activo else None

    from .routes import registrarRutas
    registrarRutas(app)

    login_manager.login_view = "auth.login"

    return app

