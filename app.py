# Autor: Hugo Martín Alonso
# Fecha: 25-09-2025
# Descripción: programa de inicialización de la aplicación.

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])