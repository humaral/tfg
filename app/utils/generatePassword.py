# Autor: Hugo Martín Alonso
# Fecha: 05/11/2025
# Descripción: Crea contraseñas temporales

import string, secrets

def temporal_password():
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(12))