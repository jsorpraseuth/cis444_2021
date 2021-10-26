from flask import Flask, render_template, request
from flask_json import FlaskJSON
from db_a3 import get_db

import bcrypt

app = Flask(__name__)
FlaskJSON(app)

JWT_SECRET = None

global_db_con = get_db()

with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/')	#endpoint
def index():
    return render_template('index.html')