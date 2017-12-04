// javascript functions to handle socket.io


// user has requested to connect to a room, handle appropriately
// create the socket, client will communicate to server that they want to enter a room
// if joining the room was succesful, the server will send a reply to all users in the room
function connect(room){
	var socket = io.connect('http://' + document.domain + ':' + location.port);
	socket.on('connect', function() {
		socket.emit('enterRoom', room);
    });

	socket.on('roomReply', function(msg){
    	alert(msg);
	});
}