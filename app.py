# Autor: Hugo Martín Alonso
# Fecha: 25-09-2025
# Descripción: Programa de inicialización de la aplicación.

from app import create_app
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
app = create_app()

if __name__ == "__main__":
    
    app.run(debug=app.config['DEBUG'])