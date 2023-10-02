from modules.shared import emit_socketio_event
import socket, json, websockets, asyncio, threading


PLUGIN_NAME = "PAtDS"
DEVELOPER_NAME = "Izitto"
TOKEN_PATH = "/home/izitto/Desktop/Code/PAtDS/vts_token.txt"
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
        print(f"VTube Studio API Server IP: {SERVER_IP}")
        print(f"VTube Studio API Server Port: {SERVER_PORT}")
    finally:
        sock.close()

async def start_websocket_connection():
    global SERVER_IP, SERVER_PORT
    while True:
        if not SERVER_IP or not SERVER_PORT:
            print("Discovering VTube Studio API Server...")
            discover_vtube_studio_server()
        
        if SERVER_IP and SERVER_PORT:
            uri = f"ws://{SERVER_IP}:{SERVER_PORT}"
            try:
                async with websockets.connect(uri) as ws:
                    print(f"Connected to VTube Studio API Server at {uri}")
                    # You can send or receive messages here using ws.send() and ws.recv()
                    # For now, let's just keep the connection alive
                    await ws.recv()
            except websockets.ConnectionClosed:
                print("Connection lost. Reconnecting...")
                SERVER_IP, SERVER_PORT = "", None  # Reset IP and port to trigger rediscovery
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(5)  # Wait for 5 seconds before retrying



# Call the function
thread = threading.Thread(target=lambda: asyncio.get_event_loop().run_until_complete(start_websocket_connection()))
def initiate_vtstudio_connection():
    global thread
    thread.start()

def stop_vtstudio_connection():
    global thread
    thread.join()