from flask import Flask, render_template, request
from flask_json import FlaskJSON, json_response
from flask.json import jsonify
from db_a3 import get_db, get_db_instance

import jwt
import bcrypt
import json

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"

app = Flask(__name__)
FlaskJSON(app)

# postgres db
db = get_db()

# declare token
TOKEN = None
JWT_SECRET = None

with open("secret", "r") as f:
    JWT_SECRET = f.read()

#----------------------------------------#
# Default Page
#----------------------------------------#

# login page and store page
@app.route('/')	# default endpoint
def index():
    return render_template('index.html')

#----------------------------------------#
# Token
#----------------------------------------#

# logout
@app.route('/logout', methods=['GET'])
def logout():
	global TOKEN
	TOKEN = None
	print("User logged out successfully.")
	return json_response(data={"message": "Logged out successfully."})


#----------------------------------------#
# Books
#----------------------------------------#



#----------------------------------------#
# Account Creation and Verification
#----------------------------------------#
	
# create user credentials
@app.route('/create', methods=['POST'])
def create():
	cur = db.cursor()
	form = request.form
	# call database to see if user exists
	cur.execute("SELECT * FROM users WHERE username = '" + jwt.encode({'username':form['username']}, JWT_SECRET, algorithm="HS256") + "';")
	# if username is available, create credentials
	if cur.fetchone() is None:
		user = jwt.encode({'username':form['username']}, JWT_SECRET, algorithm="HS256")
		encrypted_pass = bcrypt.hashpw(bytes(form['password'], 'utf-8'), bcrypt.gensalt(11))
		cur.execute("INSERT INTO users (username, password, created_on) values ('" + user + "', '" + encrypted_pass + "', current_timestamp);")
		# important commit created user to db
		db.commit()
		print('User "' + form['username'] + '" created successfully.')
		return json_response(data={"message": "User created successfully."})
	else:
		print('Error: "' + form['username'] + '" already in use.')
		return json_response(data={"message": "Username is already in use."})

# verify user credentials	
@app.route('/verify', methods=['POST'])
def verify():
	cur = db.cursor()
	form = request.form
	user = jwt.encode({'username':form['username']}, JWT_SECRET, algorithm="HS256")
	# call database to see if user exists
	cur.execute("SELECT * FROM users WHERE USERNAME = '" + user + "';")
	# stackoverflow fix :]
	row = cur.fetchone()
	# if user does not exists
	if row is None:
		print('Error: "' + form['username'] + '" does not exist.')
		return json_response(data={"message": "Username does not exist."})
	# check password
	else:
		if bcrypt.checkpw(bytes(form['password'], 'utf-8'), bytes(row[2], 'utf-8')) == True:
			print('User "' + form['username'] + '" successful login.')
			global TOKEN
			TOKEN = jwt.encode({"user_id": row[0]}, JWT_SECRET, algorithm="HS256")
			return json_response(data={"jwt": TOKEN})
		else:
			print("Incorrect password input.")
			return json_response(data={"message": "Incorrect Password. Please try again."})

app.run(host='0.0.0.0', port=80)