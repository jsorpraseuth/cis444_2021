from flask import Flask, render_template, request
from flask_json import FlaskJSON, json_response
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
	return render_template("index.html", verification="Logged out successfully.")

def validateToken(newToken):
    global TOKEN, JWT_SECRET

    if TOKEN is None:
        print("No token exists.")
        return False
    else:
        fromServer = jwt.decode(TOKEN, JWT_SECRET, algorithms=["HS256"])
        fromRequest = jwt.decode(newToken, JWT_SECRET, algorithms=["HS256"])

        if fromServer == fromRequest:
            print("Valid token.")
            return True
        else:
            print("Tokens do not match.")
            return False

#----------------------------------------#
# Books
#----------------------------------------#

@app.route('/getBooks', methods=['POST'])
def getbooks():
	if validateToken(request.form["jwt"]):
		cur = db.cursor()
		try:
			cur.execute("select * from books;")
		except:
			return json_reponse(data={"message": "Could not retrieve books from database."}, status=500)
		
		count = 0
		message = '{"books:['
		while 1:
			row = cur.fetchone()
			if row is None:
				break
			else:
				if count > 0:
					message += ","
					
				message += '{"book_id":' + str(row[0]) + ',"title:"' + str(row[1]) + ',"author:"' + str(row[2]) + ',"genre:"' + str(row[3]) + ',"price:"' + str(row[4]) + "}"
				count += 1
			
			message += "]}"
			
			print("Sending list of books")
			return json_response(data=json.loads(message))
		else:
			print("Invalid token.")
			return json_response(data={"message": "User is not logged in." }, status=404)
			
@app.route('/buyBook', methods=['POST'])
def buyBook():
	global JWT_SECRET
	decodedUser = jwt.decode(request.form["jwt"], JWT_SECRET, algorithms=["HS256"])
	cur = db.cursor()
	
	try:
		cursor.execute("insert into purchases (user_id, book_id, purchased_on) values ('" + str(decodedUser["user_id"]) + "', '" + str(request.form["book_id"]) + "', current_timestamp);'")
		db.commit()
		print("Purchase success. Sending message.")
		return json_response(data={"message": "Book bought successfully."})
	except:
		return json_response(data={"message": "Error occured while writing to database."}, status=500)

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
		return render_template("index.html", verification="Account created successfully.")
	else:
		print('Error: "' + form['username'] + '" already in use.')
		return render_template("index.html", verification="Username is already in use.")

# verify user credentials	
@app.route('/verify')
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
		return render_template("index.html", verification="Username does not exist.")
	# check password
	else:
		if bcrypt.checkpw(bytes(form['password'], 'utf-8'), bytes(row[2], 'utf-8')) == True:
			print('User "' + form['username'] + '" successful login.')
			global TOKEN
			TOKEN = jwt.encode({"user_id": row[0]}, JWT_SECRET, algorithm="HS256")
			return json_response(data={"jwt": TOKEN}, status=200)
		else:
			print("Incorrect password input.")
			return render_template("index.html", verification="Incorrect Password. Please try again.")

app.run(host='0.0.0.0', port=80)