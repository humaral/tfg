from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home(name=None):
    return render_template('login.html', person=name)
