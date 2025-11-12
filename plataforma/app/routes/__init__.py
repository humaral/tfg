# Autor: Hugo Martín Alonso
# Descripción: Inicializa el paquete routes.

from .inicio import inicio_bp
from .auth import auth_bp
from .dashboard import dashboard_bp
from .error import error_bp
from .uploads import uploads_bp

def registrarRutas(app):
    app.register_blueprint(inicio_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(uploads_bp)
    