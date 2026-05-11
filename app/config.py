# Autor: Hugo Martín Alonso
# Fecha: 23-11-2025
# Descripción: Archivo con las configuraciones de la aplicación.

import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY', "clave_local_para_desarollo")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "data")
    os.makedirs(DB_PATH, exist_ok=True)

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(DB_PATH, 'data.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = ("Trámites Telefónicos", "noreply@tramitestelefonicos.es")
    MAIL_SUPPRESS_SEND = False

    APP_VERSION = "0.1 \u03B2"

    DEBUG = True
    REINICIAR_BD_ON_STARTUP = False