# Autor: Hugo Martín Alonso
# Descripción: programa de inicialización de la aplicación.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from datetime import datetime
from .routes import registrarRutas #NOTE Igual tiene que ir dentro de la función
db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    #TODO REVISAR DONDE IRÁ ESTO
    #Se establecen variables globales en las plantillas que se actualizan al refrescar la página
    @app.context_processor
    def inject_globals():
        return {
            "current_date": datetime.now().strftime('%d/%m/%Y'),
            "current_year": datetime.now().year
        }
    
    registrarRutas(app)

    return app

