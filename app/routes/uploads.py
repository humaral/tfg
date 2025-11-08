# Autor: Hugo Martín Alonso
# Fecha: 28/10/2025
# Descripción: Controlador de las rutas relacionadas con la subida de archivos a la app.

from flask import Blueprint, send_from_directory, current_app, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db


uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/uploads/perfil/<filename>')
@login_required
def fotoPerfil(filename):

    ruta = os.path.join(current_app.root_path, 'uploads', 'perfil')
    
    return send_from_directory(ruta, filename)


def borrarFotoPerfil(filename):
    if not(filename) or filename=="default.jpg":
        return
    
    ruta = os.path.join(current_app.root_path, 'uploads', 'perfil', filename)
    if os.path.exists(ruta):
        os.remove(ruta)


@uploads_bp.route('/uploads/perfil', methods=["POST"])
@login_required
def subirFotoPerfil():

    foto = request.files['foto_perfil']
    extension = foto.mimetype.rsplit('/',1)[1]
    filename = secure_filename(f"{current_user.username}.{extension}")

    borrarFotoPerfil(current_user.fotoPerfil)

    ruta = os.path.join(current_app.root_path, 'uploads', 'perfil', filename)
    
    foto.save(ruta)
    current_user.fotoPerfil = filename
    db.session.commit()

    return jsonify({"success": True})
