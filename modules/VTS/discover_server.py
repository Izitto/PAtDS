import socket, json
from modules.shared import emit_socketio_event
SERVER_IP = ""
SERVER_PORT = None

def discover_vtube_studio_server():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = ('0.0.0.0', 47779)  # 0.0.0.0 means all available interfaces
    sock.bind(server_address)

    print("Waiting for VTube Studio API Server Discovery broadcast...")

    try:
        # Receive data from the socket (up to 4096 bytes)
        data, address = sock.recvfrom(4096)
        # Decode the received data to string and parse it as JSON
        message = json.loads(data.decode('utf-8'))
        # Extract the server IP and port from the message
        global SERVER_IP, SERVER_PORT
        SERVER_IP = address[0]
        SERVER_PORT = message.get('data', {}).get('port', None)
        emit_socketio_event("vts_debug", f"VTube Studio API Server discovered at {SERVER_IP}:{SERVER_PORT}")
    finally:
        sock.close()