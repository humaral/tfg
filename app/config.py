# Autor: Hugo Martín Alonso
# Descripción: archivo con las configuraciones de la aplicación.

import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY', "clave_local_para_desarollo")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(BASE_DIR, "datos")
    os.makedirs(db_path, exist_ok=True)

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(db_path, 'datos.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_VERSION = "0.1 \u03B2"

    DEBUG = True
