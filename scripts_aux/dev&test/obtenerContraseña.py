# Autor: Hugo Martín Alonso
# Fecha: 30-10-2025
# Descripción: Script para generar el hash de una contraseña, útil para poder añadir contraseñas manualmente en la base de datos para el desarrollo.

from werkzeug.security import generate_password_hash


print(generate_password_hash("admin"))
