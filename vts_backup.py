from modules.shared import emit_socketio_event
import socket, json, websockets, asyncio, threading


PLUGIN_NAME = "PAtDS"
DEVELOPER_NAME = "Izitto"
TOKEN_PATH = "/home/izitto/Desktop/Code/PAtDS/vts_token.txt"
SERVER_IP = ""
SERVER_PORT = None
VTS_MODELS = []
IS_CONNECTED = False
ws = websockets

# function variables
req_model_id = None
req_expressionFile = None
req_hotkeyID = None

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
    finally:
        sock.close()

async def authenticate_with_server(ws):
    # Check if there's an authentication token in the text file
    try:
        with open(TOKEN_PATH, 'r') as token_file:
            token = token_file.read().strip()
    except FileNotFoundError:
        token = None

    # If no token found, request one from the server
    if not token:
        auth_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": PLUGIN_NAME,
                "pluginDeveloper": DEVELOPER_NAME,
            }
        }
        await ws.send(json.dumps(auth_request))
        response = await ws.recv()
        response_data = json.loads(response)
        # If a token is received from the server, store it in the text file
        if response_data.get('data', {}).get('authenticationToken'):
            token = response_data['data']['authenticationToken']
            with open(TOKEN_PATH, 'w') as token_file:
                token_file.write(token)

        
    # Send the token to the server to authenticate the plugin connection
    if token:
        token_send_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": PLUGIN_NAME,
                "pluginDeveloper": DEVELOPER_NAME,
                "authenticationToken": token
            }
        }
        await ws.send(json.dumps(token_send_request))
    response = await ws.recv()
    response_data = json.loads(response)
    if response_data.get('data', {}).get('currentSessionAuthenticated') == "true":
        return True
    else:
        return False


async def fetch_vts_models(ws):
    model_request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "AvailableModelsRequest"
    }
    await ws.send(json.dumps(model_request))
    response = await ws.recv()
    response_data = json.loads(response)
    

    # Extract model names and IDs and store them in the global VTS_MODELS array
    global VTS_MODELS
    VTS_MODELS = [{"name": model["modelName"], "id": model["modelID"]} for model in response_data.get('data', {}).get('availableModels', [])]
    emit_socketio_event("vts_debug", VTS_MODELS)

# subscribe to events
async def loadModel(ws, Model_ID):
    load_model_request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "LoadModelRequest",
        "data": {
            "modelID": Model_ID
        }
    }
    await ws.send(json.dumps(load_model_request))
    response = await ws.recv()
    response_data = json.loads(response)
    emit_socketio_event("vts_debug", response_data)



async def start_websocket_connection():
    global SERVER_IP, SERVER_PORT, req_expressionFile, req_hotkeyID, req_model_id
    authenticated = False
    models_fetched = False
    
    while True:
        if not SERVER_IP or not SERVER_PORT:
            emit_socketio_event("vts_debug", "Discovering VTube Studio API Server...")
            discover_vtube_studio_server()
        
        if SERVER_IP and SERVER_PORT:
            uri = f"ws://{SERVER_IP}:{SERVER_PORT}"
            # emit_socketio_event("vts_debug", f"Connecting to VTube Studio API Server at {uri}...")
            try:
                async with websockets.connect(uri) as ws:
                    print(f"Connected to VTube Studio API Server at {uri}")
                    if authenticated == False:
                        authenticated = await authenticate_with_server(ws)

                    # You can send or receive messages here using ws.send() and ws.recv()
                    # For now, let's just keep the connection alive
                    
                    
                    if models_fetched == False:
                        await fetch_vts_models(ws)
                        models_fetched = True
                    await ws.recv()
            
            except websockets.ConnectionClosed:
                print("Connection lost. Reconnecting...")
                authenticated, models_fetched = False
                SERVER_IP, SERVER_PORT = "", None  # Reset IP and port to trigger rediscovery
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(5)  # Wait for 5 seconds before retrying

# Call the function
def initiate_vtstudio_connection():
    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_websocket_connection())

    thread = threading.Thread(target=run)
    thread.start()
    return thread
