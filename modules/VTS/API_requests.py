import json, queue
from modules.VTS.model import Model, Models
from modules.VTS.expression import Expression, Expressions
from modules.shared import emit_socketio_event
req_model_id = None
req_expression = { "file": None, "status": None}
req_hotkeyID = None
models_fetched = False
expressions_fetched = False
PLUGIN_NAME = "PAtDS"
DEVELOPER_NAME = "Izitto"
TOKEN_PATH = "/home/izitto/Desktop/Code/PAtDS/vts_token.txt"
VTS_MODELS = Models()
VTS_EXPRESSIONS = Expressions()
send = queue.Queue()
IS_CONNECTED = False
IS_AUTH = False

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
    return [Model(model["modelName"], model["modelID"], model["modelLoaded"]) for model in response_data.get('data', {}).get('availableModels', [])]

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
    return [Expression(expression["name"], expression["file"], expression["active"]) for expression in response_data.get('data', {}).get('expressionState', [])]


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
    if req_expression['file'] != None and req_expression['status'] != None:
        await ws.send(json.dumps(header))
        response = await ws.recv()
        response_data = json.loads(response)
        emit_socketio_event("vts_debug", response_data)
        req_expression = { "file": None, "status": None}


