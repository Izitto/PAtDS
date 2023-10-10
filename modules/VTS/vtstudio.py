from modules.shared import emit_socketio_event
import socket, json, websockets, asyncio, threading
import modules.shared as shared
import queue

PLUGIN_NAME = "PAtDS"
DEVELOPER_NAME = "Izitto"
TOKEN_PATH = "/home/izitto/Desktop/Code/PAtDS/vts_token.txt"
SERVER_IP = ""
SERVER_PORT = None
VTS_MODELS = []
VTS_EXPRESSIONS = []
IS_CONNECTED = False
IS_AUTH = False
ws = websockets
# function variables
req_model_id = None
req_expression = None
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
        emit_socketio_event("vts_debug", f"VTube Studio API Server discovered at {SERVER_IP}:{SERVER_PORT}")
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
        header = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": PLUGIN_NAME,
                "pluginDeveloper": DEVELOPER_NAME,
            }
        }
        await ws.send(json.dumps(header))
        response = await ws.recv()
        response_data = json.loads(response)
        # If a token is received from the server, store it in the text file
        if response_data.get('data', {}).get('authenticationToken'):
            token = response_data['data']['authenticationToken']
            with open(TOKEN_PATH, 'w') as token_file:
                token_file.write(token)

        
    # Send the token to the server to authenticate the plugin connection
    if token:
        header = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": PLUGIN_NAME,
                "pluginDeveloper": DEVELOPER_NAME,
                "authenticationToken": token
            }
        }
        await ws.send(json.dumps(header))
    response = await ws.recv()
    response_data = json.loads(response)
    if response_data.get('data', {}).get('currentSessionAuthenticated') == "true":
        return True
    else:
        return False


async def fetch_vts_models(ws):
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "AvailableModelsRequest"
    }
    await ws.send(json.dumps(header))
    response = await ws.recv()
    response_data = json.loads(response)
    # Extract model names and IDs and store them in the global VTS_MODELS array
    # global VTS_MODELS
    return [{"name": model["modelName"], "id": model["modelID"], "active": model["modelLoaded"]} for model in response_data.get('data', {}).get('availableModels', [])]

async def fetch_vts_expressions(ws):
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "SomeID",
        "messageType": "ExpressionStateRequest",
        "data": {
            "details": True,
            "expressionFile": "myExpression_optional_1.exp3.json",
        }
    }
    await ws.send(json.dumps(header))
    response = await ws.recv()
    response_data = json.loads(response)
    # Extract extract name, file and active status and store them in the global VTS_EXPRESSIONS array
    # global VTS_EXPRESSIONS
    return [{"name": expression["name"], "file": expression["file"], "active": expression["active"]} for expression in response_data.get('data', {}).get('expressionState', [])]


async def loadModel(ws):
    global req_model_id
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "ModelLoadRequest",
        "data": {
            "modelID": req_model_id
        }
    }
    if req_model_id != None:
        await ws.send(json.dumps(header))
        response = await ws.recv()
        response_data = json.loads(response)
        emit_socketio_event("vts_debug", response_data)
        req_model_id = None

async def setExpression(ws):
    global req_expression
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "SetExpressionRequest",
        "data": {
            "expressionFile": req_expression['file'],
            "active": req_expression['status']
        }
    }
    if req_expression != None:
        await ws.send(json.dumps(header))
        response = await ws.recv()
        response_data = json.loads(response)
        emit_socketio_event("vts_debug", response_data)
        req_expression = []



async def start_websocket_connection():
    global SERVER_IP, SERVER_PORT, IS_AUTH, IS_CONNECTED, VTS_MODELS, VTS_EXPRESSIONS
    models_fetched = False
    expressions_fetched = False
    
    while True:
        
        if not SERVER_IP or not SERVER_PORT:
            emit_socketio_event("vts_debug", "Discovering VTube Studio API Server...")
            discover_vtube_studio_server()
        
        if SERVER_IP and SERVER_PORT:
            uri = f"ws://{SERVER_IP}:{SERVER_PORT}"
            # emit_socketio_event("vts_debug", f"Connecting to VTube Studio API Server at {uri}...")
            try:
                emit_socketio_event("vts_debug", f"Connecting to VTube Studio API Server at {uri}...")
                async with websockets.connect(uri) as ws:
                    IS_CONNECTED = True
                    emit_socketio_event("vts_debug", "Connected!")
                    if IS_AUTH == False:
                        IS_AUTH = await authenticate_with_server(ws)

                    # You can send or receive messages here using ws.send() and ws.recv()
                    # For now, let's just keep the connection alive
                    await loadModel(ws)
                    await setExpression(ws)
                    
                    if expressions_fetched == False:
                        VTS_EXPRESSIONS = await fetch_vts_expressions(ws)
                        expressions_fetched = True
                    
                    if models_fetched == False:
                        VTS_MODELS = await fetch_vts_models(ws)
                        models_fetched = True
                    response = await ws.recv()
                    emit_socketio_event("vts_debug", response)
            
            except websockets.ConnectionClosed:
                emit_socketio_event("vts_debug", "Connection closed")
                IS_AUTH = False
                IS_CONNECTED = False
                SERVER_IP, SERVER_PORT = "", None  # Reset IP and port to trigger rediscovery
            except Exception as e:
                emit_socketio_event("vts_debug", f"Error: {e} {type(e)} {e.args} {e.__traceback__.tb_lineno}")
                IS_AUTH = False
                IS_CONNECTED = False
                await asyncio.sleep(5)  # Wait for 5 seconds before retrying
                

# Call the function
def initiate_vtstudio_connection():
    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_websocket_connection())

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
    return thread



# requests
def model_request(model_id):
    global req_model_id
    req_model_id = model_id


def expression_request(file, active):
    global req_expression
    req_expression = [file, active]
