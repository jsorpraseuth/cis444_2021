from flask import Flask, render_template, request
from flask_json import FlaskJSON, json_response
from db_a3 import get_db, get_db_instance

import json
import jwt
import bcrypt
import datetime

app = Flask(__name__)
FlaskJSON(app)

# postgres db
db = get_db()

TOKEN = None
SECRET = None

with open("secret", "r") as f:
    SECRET = f.read()

#----------------------------------------#
# Index page
#----------------------------------------#
# login page and store page
@app.route("/")	# default endpoint
def index():
	return render_template("index.html")
	
#----------------------------------------#
# User Verification
#----------------------------------------#

# checks if username is taken, adds user to database
@app.route("/signup", methods=["POST"])
def signup():
	cur = db.cursor()
	form = request.form
	username = request.form["username"]
	password = request.form["password"]
	
	try:
		cur.execute("select * from users where username = '" + username + "';")
	except:
		return json_response(data = {"message" : "Database could not be accessed."}, status = 500)
	
	if cur.fetchone() is None:
		saltedPassword = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt(11))
		try:
			cur.execute("insert into users (username, password, created_on) values '" + username + "', " + saltedPassword.decode("utf-8") + "', current_timestamp;")
			db.commit()
			print("Created user '" + username + "'.")
			return json_response(data = {"message" : "User created successfully."})
		except:
			return json_response(data = {"message" : "Could not reach database to create user."})
	else:
		print("Username '" + username + "' taken,")
		return json_response(data = {"message" : "Username '" + username + "' already in use."})

# check if user exists, create jwt token from user id
@app.route("/login", methods=["POST"])
def login():
	cur = db.cursor()
	
	try:
		cur.execute("select * from users where username = '" + request.form["username"] + "';")
	except:
		return json_response(data = {"message" : "Database could not be accessed."}, status = 500)
	
	row = cur.fetchone()
	
	if row is None:
		print("Username '" + request.form["username"] + "' is invalid.")
		return json_response(data = {"message" : "Username '" + request.form["username"] + "' does not exist."}, status = 404)
	else:
		if bcrypt.checkpw(bytes(request.form["password"], "utf-8"), bytes(row[2], "utf-8")) == True:
			print("Login by '" + request.form["username"] + "' authorized.")
			global TOKEN, SECRET
			TOKEN = jwt.encode({"user_id": row[0]}, SECRET, algorithm="HS256")
			return json_response(data = {"jwt" : TOKEN})
		else:
			print("Incorrect password.")
			return json_response(data = {"message" : "Incorrect passowrd."}, status = 404)


app.run(host = '0.0.0.0', port = 80)