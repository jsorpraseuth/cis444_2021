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

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)