function connect(room){
	var socket = io.connect('http://' + document.domain + ':' + location.port);
	socket.on('connect', function() {
		socket.emit('enterRoom', room);
    });

	socket.on('roomReply', function(msg){
    	alert(msg);
	});
}