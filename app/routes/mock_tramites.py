# Autor: Hugo Martín Alonso
# Fecha: 18-11-2025
# Descripción: Controlador de las rutas relacionadas con las copias de las páginas donde se realizan los trámites.
#DELETE
from flask import Blueprint, render_template


mock_tramties_bp = Blueprint('mock_tramites', __name__, url_prefix="/mock")


@mock_tramties_bp.route("/Certificado_De_Empadronamiento", methods=["GET","POST"])
def empadronamiteno():
    return render_template("mock_tramites/empadronamiento.html")