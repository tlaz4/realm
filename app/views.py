from flask import render_template
from app import app
from .dungeonGen import getDungeon
from .stringGen import genString
import socketio
import eventlet

sio = socketio.Server()

sessionRooms = []

# where users can join room, for development also displays this sessions randomly generated map
@app.route('/')
@app.route('/index')
def index():
	rooms = getDungeon()

	roomCoords = rooms[0]
	hollowedRooms = rooms[1]

	return render_template('index.html', roomCoords = roomCoords, hollowedRooms = hollowedRooms, sessionRooms = sessionRooms)

# create a new room, where the room name is a randomly generated 4 char string
@app.route('/create')
def create():
	rndStr = genString()

	return render_template('create.html', rndStr = rndStr)

# a user has connected to the application
@sio.on('connect')
def connect(sid, data):
	print(sid + " is connected.")

# when a user enters a room, emit to all users that a user has joined
# if the room is a new room, we will add it to the list of rooms (for testing purposes, real implementation
# wont require the server to keep track of all rooms)
@sio.on('enterRoom')
def message(sid, data):
	print(sid + " has joined " + data)
	sio.enter_room(sid, data)
	sio.emit("roomReply", "welcome to room " + data, data)
	# for testing
	if data not in sessionRooms:
		sessionRooms.append(data)

@sio.on('disconnect')
def disconnect(sid):
	print('disconnect ', sid)

# wrap Flask application with socketio's middleware
app = socketio.Middleware(sio, app)

# deploy as an eventlet WSGI server
eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
