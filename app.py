from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)


@app.route('/')
def init_app(name=None):
    DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')


@app.route('/login')
def login(name=None):

    return render_template('login.html', person=name)