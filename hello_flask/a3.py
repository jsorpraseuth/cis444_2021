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
	# call database to see if user exists
	cur.execute("SELECT * FROM users WHERE username = '" + request.form["username"] + "';")
	# if username is available, create credentials
	if cur.fetchone() is None:
		user = request.form["username"]
		encrypted_pass = bcrypt.hashpw(bytes(form['password'], 'utf-8'), bcrypt.gensalt(11))
		cur.execute("INSERT INTO users (username, password, created_on) values ('" + user + "', '" + encrypted_pass + "', current_timestamp);")
		# important commit created user to db
		db.commit()
		print('User "' + form['username'] + '" created successfully.')
		return json_response(data = {"message" : "User account created successfully."})
	else:
		print('Error: "' + form['username'] + '" already in use.')
		return json_response(data = {"message" : "Username is already in use."}, status = 404)

# check if user exists, create jwt token from user id
@app.route("/login", methods=["POST"])
def login():
	cur = db.cursor()
	form = request.form
	# call database to see if user exists
	cur.execute("select * from users where username = '" + request.form["username"] + "';")
	row = cur.fetchone()
	# if username invalid, error
	if row is None:
		print("Username '" + form["username"] + "' is invalid.")
		return json_response(data = {"message" : "Username '" + form["username"] + "' does not exist."}, status = 404)
	# username exists, make a token
	else:
		if bcrypt.checkpw(bytes(form["password"], "utf-8"), bytes(row[2], "utf-8")) == True:
			print("Login by '" + form["username"] + "' authorized.")
			global TOKEN, SECRET
			TOKEN = jwt.encode({"user_id": row[0]}, SECRET, algorithm="HS256")
			return json_response(data = {"jwt" : TOKEN})
		else:
			print("Incorrect password.")
			return json_response(data = {"message" : "Incorrect password."}, status = 404)

# token validation
def validToken(tok):
	global TOKEN, SECRET
	if TOKEN is None:
		print("No token available in server.")
		return false
	else:
		server = jwt.decode(TOKEN, SECRET, algorithms=["HS256"])
		client = jwt.decode(tok, SECRET, algorithms=["HS256"])
		
		if server == client:
			print("Token authorized.")
			return True
		else:
			print("Invalid token.")
			return False

#----------------------------------------#
# Bookstore
#----------------------------------------#

# load list of books after successful login
@app.route("/loadBooks", methods=["POST"])
def loadBooks():
	if validToken(request.form["jwt"]) == True:
		print("Token is true, loading books")
		cur = db.cursor()
		
		try:
			# grab books from db
			cur.execute("select * from books;")
			print("Grabbed books from database.")
		except:
			print("Could not find books from database.")
			return json_response(data = {"message" : "Could not find books from database."}, status = 500)
			
		# loop and show all books
		count = 0
		message = '{"books":['
		while 1:
			row = cur.fetchone()
			if row is None:
				return json_response(data = {"message": "There are no books to display."}, status = 500)
			else:
				if count > 0:
					message += ","
				message += '{"book_name":' + row[1] + ',"book_author":"' + str(row[2]) + + '","book_genre":' + row[3] + '","book_price":' + row[4] + "}"
				count += 1
				print("Grabbed a book. " + title)
				
		message += "]}"
		
		print("Loading books")
		return json_response(data = json.loads(message))
	else:
		print("Invalid token. Will not send book list.")
		return json_response(data = {"message" : "Invalid session token."}, status = 404)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

app.run(host = '0.0.0.0', port = 80)