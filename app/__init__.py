# Autor: Hugo Martín Alonso
# Descripción: programa de inicialización de la aplicación.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager #TODO CAMBIAR LOGIN A FLASK_LOGIN
from .config import Config
from datetime import datetime


db = SQLAlchemy()
login_manager = LoginManager()
# login_manager.login_view = "auth.login"

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # login_manager.init_app(app)

    #TODO REVISAR DONDE IRÁ ESTO
    #Se establecen variables globales en las plantillas que se actualizan al refrescar la página
    @app.context_processor
    def inject_globals():
        return {
            "current_date": datetime.now().strftime('%d/%m/%Y'),
            "current_year": datetime.now().year
        }
    
    from app import models

    from .routes import registrarRutas #NOTE Igual tiene que ir dentro de la función
    registrarRutas(app)

    return app

