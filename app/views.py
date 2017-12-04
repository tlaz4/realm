from flask import render_template
from app import app
from .dungeonGen import getDungeon
import socketio
import eventlet

sio = socketio.Server()

@app.route('/')
@app.route('/index')

def index():
	rooms = getDungeon()

	roomCoords = rooms[0]
	hollowedRooms = rooms[1]

	return render_template('index.html', roomCoords = roomCoords, hollowedRooms = hollowedRooms)

@sio.on('connect')
def connect(sid, data):
	print(sid + " is connected.")

@sio.on('enterRoom')
def message(sid, data):
    print(sid + " has joined " + data)
    sio.enter_room(sid, data)
    sio.emit("roomReply", "welcome to room " + data, data)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

# wrap Flask application with socketio's middleware
app = socketio.Middleware(sio, app)

# deploy as an eventlet WSGI server
eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
