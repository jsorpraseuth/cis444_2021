from flask import Flask,render_template,request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room
from flask_json import FlaskJSON, json_response
from db import get_db

import json
import jwt
import bcrypt
import datetime

app = Flask(__name__)
FlaskJSON(app)
socketio = SocketIO(app)

# postgres db
db = get_db()

# default page
@app.route('/')
def home():
    return render_template("index.html")

# chat page
@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])

@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])

# credentials
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
        return json_response(data={"message": "Username '" + form["username"] + "' does not exist."}, status=404)
    # username exists, make a token
    else:
        if bcrypt.checkpw(bytes(form["password"], "utf-8"), bytes(row[1], "utf-8")) == True:
            print("Login by '" + form["username"] + "' authorized.")
            # update last login by user
            cur.execute("update users set last_login = current_timestamp where username = '" + form["username"] + "';")
            db.commit();
            global TOKEN, SECRET
            TOKEN = jwt.encode({"user_id": row[0]}, SECRET, algorithm="HS256")
            return json_response(data={"jwt": TOKEN})
        else:
            print("Incorrect password.")
            return json_response(data={"message": "Incorrect password."}, status=404)


# token validation
def validToken(tok):
    global TOKEN, SECRET
    if TOKEN is None:
        print("No token available in server.")
        return False
    else:
        server = jwt.decode(TOKEN, SECRET, algorithms=["HS256"])
        client = jwt.decode(tok, SECRET, algorithms=["HS256"])

        if server == client:
            print("Token authorized.")
            return True
        else:
            print("Invalid token.")
            return False


# logout user
@app.route("/logout", methods=["GET"])
def logout():
    global TOKEN
    TOKEN = None
    print("User logged out.")
    return json_response(data={"message": "Logged out."})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)