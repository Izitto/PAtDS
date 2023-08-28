const output = document.getElementById('output');

/* const source = new EventSource('{{url_for('static', filename='log.txt')}}');



source.onmessage = (event) => {

    output.innerHTML += event.data + '<br>';

    output.scrollTop = output.scrollHeight;

};
*/


class UDP {

    constructor(port) {

        this.socket = new WebSocket('ws://localhost:' + port);

        this.socket.onmessage = (event) => {

            const message = event.data;

            // handle message

        };

    }

    send(message) {

        this.socket.send(message);

    }

}
const udp = new UDP(20002);
