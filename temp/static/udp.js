var socket = io.connect('http://' + document.domain + ':80');

socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('disconnect', function() {
    console.log('Disconnected from server');
});

socket.on('udp_packet', function(data) {
    console.log('Received UDP packet:', data);
});




/*
const ws = new WebSocket('ws://192.168.1.107:19999', 'udp');

console.log("1");
const friends = ['Izitto', 'Bob', 'Charlie'];
console.log("2");
const friendlist = [];
let friend = null;
let viewer = null;

try{ 
ws.addEventListener('message', event => {
    const message = event.data;
    console.log("3");
    // Read the contents of the file
    fetch("{{url_for('static', filename='friends.txt')}}")
        .then(response => response.text())
        .then(text => {
        // Split the file contents into an array of messages
        const friends = text.split('\n');
        console.log("4");
        // Check if the message exists in the file
        if (friends.includes(message)) {
            // If it does, pass the message to the 'friend' string
            friendlist.push(message);
            console.log('Message received from friend:', friend);
        } else {
            // Otherwise, pass the message to the 'viewer' string
            viewer = message;
            console.log('Message received from viewer:', viewer);
        }
    });
});
} catch ( e ) {
    fallback();
    console.warn(e);
}
console.log("");
setInterval(() => {
  if (friendlist.length > 0) {
    friend = friendlist.shift();
    console.log(`Popped ${friend} from friendlist`);
  } else {
    friend = null;
  }
}, 3000);

*/