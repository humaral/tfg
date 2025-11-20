# Autor: Hugo Martín Alonso
# Descripción: archivo con las configuraciones de la aplicación.

import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY', "clave_local_para_desarollo")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "data")
    os.makedirs(DB_PATH, exist_ok=True)

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(DB_PATH, 'data.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_VERSION = "0.1 \u03B2"

    DEBUG = True
    REINICIAR_BD_ON_STARTUP = True