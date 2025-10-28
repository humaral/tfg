# Autor: Hugo Martín Alonso
# Fecha: 28/10/2025
# Descripción: Controlador de las rutas relacionadas con la subida de archivos a la app.

from flask import Blueprint, abort, send_from_directory, current_app
from flask_login import current_user
import os


uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/uploads/perfil/<filename>')
#TODO poner: @login_required
def fotoPerfil(filename):

    ruta = os.path.join(current_app.root_path, 'uploads', 'perfil')
    
    return send_from_directory(ruta, filename)