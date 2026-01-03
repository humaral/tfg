# Autor: Hugo Martín Alonso
# Descripción: programa de inicialización de la aplicación.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_login import LoginManager
from flask_mail import Mail
from .config import Config
from datetime import datetime
import csv, os

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

        with open(os.path.join(app.root_path, "data/centros_salud_vall.csv"), newline="", encoding="utf-8") as f:
            centros_salud_vall = list(csv.DictReader(f))
        with open(os.path.join(app.root_path, "data/municipios_vall.csv"), newline="", encoding="utf-8") as f:
            municipios_vall = list(csv.DictReader(f))
        with open(os.path.join(app.root_path, "data/oficina_aeat_vall.csv"), newline="", encoding="utf-8") as f:
            oficinas_aeat_vall = list(csv.DictReader(f))
        with open(os.path.join(app.root_path, "data/servicios_aeat.csv"), newline="", encoding="utf-8") as f:
            servicios_aeat = list(csv.DictReader(f, delimiter=';'))
            
        return {
            "current_date": datetime.now().strftime('%d/%m/%Y'),
            "current_year": datetime.now().year,
            "centros_salud_vall": centros_salud_vall,
            "municipios_vall": municipios_vall,
            "oficinas_aeat_vall": oficinas_aeat_vall,
            "servicios_aeat": servicios_aeat
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

