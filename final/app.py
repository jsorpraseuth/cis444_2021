from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from db import get_db_instance, get_db

app = Flask(__name__)
socketio = SocketIO(app)

# g is flask for a global var storage 
def init_new_env():
	if 'db' not in g:
		g.db = get_db()
		
	g.secrets = get_secrets()

@app.route('/')
def home():
	return render_template("index.html")
	
@app.route('/chat')
def chat():
	username = request.args.get('username')
	room = request.args.get('room')
	
	if username and room:
		return render_template('chat.html', username = username, room = room)
	else:
		return redirect(url_for('home'))
	
@socketio.on('send_message')
def handle_send_message_event(data):
	app.logger.info("{} has sent message to room {}: {}".format(data['username'], data['room'], message['message']))
	socket.io.emit('receive_message', data, room = data['room'])
	
@socketio.on('join_room')
def handle_join_room_event(data):
	app.logger.info("{} has joined room {}.".format(data['username'], data['room']))
	join_room(data['room'])
	socketio.emit('join_notification', data['username'])
	
if __name__ == '__main__':
	socketio.run(host = '0.0.0.0', port = 80, app)