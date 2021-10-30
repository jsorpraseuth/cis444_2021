from flask import Flask, render_template, request
from flask_json import FlaskJSON, json_response
from db_a3 import get_db

import json
import jwt
import bcrypt
import datetime

app = Flask(__name__)
FlaskJSON(app)

TOKEN = None
SECRET = None

with open("secret", "r") as f:
    SECRET = f.read()

# postgres db
db = get_db()

#----------------------------------------#
# Index page
#----------------------------------------#
# login page and store page
@app.route('/')	# default endpoint
def home():
	return 
	
#----------------------------------------#
# User Verification
#----------------------------------------#

# checks if username is taken, adds user to database
@app.route('/signup', methods=["POST"])
def signup():
	cur = db.cursor()
	
	try:
		cur.execute("select * from users where username = '" + request.form["username"] + "';")
	except:
		return json_response(data = {"error" : "Database could not be accessed."}, status = 500)
		
	if cur.fetchOne() is None:
		saltedPassword = bcrypt.hashpw(bytes(request.form["password"], "utf-8"), bcrypt.gensalt(11))
		try:
			cur.execute("insert into users (username, password, created_on) values '" + request.form["username"] + "', " + saltedPassword.decode("utf-8") + "', current_timestamp;")
			db.commit()
			print("Created user '" + request.form["username"] + "'.")
			return json_response(data = {"success" : "User created successfully."})
		except:
			return json_response(data = {"error" : "Could not reach database to create user."})
	else:
		print("Username '" + request.form["username"] + "' taken,")
		return json_response(data = {"error" : "Username '" + request.form["username"] + "' already in use."

app.run(host = '0.0.0.0', port = 80)