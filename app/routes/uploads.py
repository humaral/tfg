# Autor: Hugo Martín Alonso
# Fecha: 28/10/2025
# Descripción: Controlador de las rutas relacionadas con la subida de archivos a la app.

from flask import Blueprint, send_from_directory, current_app, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os


uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/uploads/perfil/<filename>')
@login_required
def fotoPerfil(filename):

    ruta = os.path.join(current_app.root_path, 'uploads', 'perfil')
    
    return send_from_directory(ruta, filename)

# TODO acabar subida de foto de perfil
# @uploads_bp.route('/uploads/perfil', methods=["POST"])
# @login_required
# def subirFotoPerfil():
#     foto = request.files['foto_perfil']
#     extension = foto.filename.rsplit('.',1)[1].lower()
#     filename = secure_filename(f"{current_user.username}.{extension}")

#     ruta = os.path.join(current_app.root_path, 'uploads', 'perfil', filename)

#     foto.save(ruta)
#     print(foto)
#     return
