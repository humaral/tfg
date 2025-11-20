# Autor: Hugo Martín Alonso
# Descripción: Inicializa el paquete utils.

from .permisos import (
    cargar_permisos,
    permiso_requerido,
    verificar_permiso
)

from .dashboard_utils import(
    temporal_password,
    crear_peticion
)

from .rpa import(
    rpa_certificado_empadronamiento
)

from .reiniciarBD import(
    reiniciar_bd)