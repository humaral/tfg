from flask import Flask, render_template, jsonify
import os
from datetime import datetime

APP_VERSION = "0.1"

app = Flask(__name__)

@app.context_processor
def inject_globals():
    return {
        "current_date": datetime.now().strftime('%d/%m/%Y'),
        "current_year": datetime.now().year,
        "version": APP_VERSION
    }

@app.route('/')
def inicio(name=None):
    DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    return render_template('index.html', person=name, database=DATABASE)

@app.route('/login')
def login(name=None):

    return render_template('login.html', person=name)

if __name__ == "__main__":
    app.run(debug=True)