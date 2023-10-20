import json, queue
from modules.VTS.objects import VTS_MODELS, VTS_EXPRESSIONS, Model, Expression
from modules.shared import emit_socketio_event
req_model_id = None
req_expression = { "file": None, "status": None}
req_hotkeyID = None
models_fetched = False
expressions_fetched = False
PLUGIN_NAME = "PAtDS"
DEVELOPER_NAME = "Izitto"
TOKEN_PATH = "/home/izitto/Desktop/Code/PAtDS/vts_token.txt"
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

    global IS_AUTH
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
    if response_data.get('data', {}).get('authenticated') is True:
        emit_socketio_event("vts_debug", "Authenticated with VTube Studio")
    else:
        emit_socketio_event("vts_debug", "Authentication with VTube Studio failed")
        emit_socketio_event("vts_debug", response_data)


async def fetch_vts_models(ws):
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "AvailableModelsRequest"
    }
    try:
        await ws.send(json.dumps(header))
        response = await ws.recv()
        response_data = json.loads(response)
        # Extract model names and IDs and store them in the global VTS_MODELS array
        # add models
        VTS_MODELS.addModels([Model(model["modelName"], model["modelID"], model["modelLoaded"]) for model in response_data.get('data', {}).get('availableModels', [])])
        # emit_socketio_event("vts_debug", VTS_MODELS.toStr())
    except Exception as e:
        emit_socketio_event("vts_debug", f"Error: {e} {type(e)} {e.args} {e.__traceback__.tb_lineno}")


async def fetch_vts_expressions(ws):
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "SomeID",
        "messageType": "ExpressionStateRequest",
        "data": {
            "details": True
        }
    }
    try:
        await ws.send(json.dumps(header))
        response = await ws.recv()
        response_data = json.loads(response)
        # Extract extract name, file and active status and store them in the global VTS_EXPRESSIONS array
        # Expressions.addExpression([Expression(expression["name"], expression["file"], expression["active"]) for expression in response_data.get('data', {}).get('expressionState', [])])
        # add expressions
        VTS_EXPRESSIONS.addExpressions([Expression(expression["name"], expression["file"], expression["active"]) for expression in response_data.get('data', {}).get('expressions', [])])
        # emit_socketio_event("vts_debug", VTS_EXPRESSIONS.toStr())
        # emit_socketio_event("vts_debug", response_data)
    except Exception as e:
        emit_socketio_event("vts_debug", f"Error: {e} {type(e)} {e.args} {e.__traceback__.tb_lineno}")

async def loadModel(ws, model_id):
    # global req_model_id
    emit_socketio_event("vts_debug", "model requested: " + model_id)
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "ModelLoadRequest",
        "data": {
            "modelID": model_id
        }
    }
    await ws.send(json.dumps(header))
    # response = await ws.recv()
    # response_data = json.loads(response)
    # emit_socketio_event("vts_debug", response_data)

async def setExpression(ws, expression):
    # global req_expression
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "SetExpressionRequest",
        "data": {
            "expressionFile": expression['file'],
            "active": expression['status']
        }
    }
    # if req_expression['file'] != None and req_expression['status'] != None:
    await ws.send(json.dumps(header))
    # response = await ws.recv()
    # response_data = json.loads(response)
    # emit_socketio_event("vts_debug", response_data)
    # expression = { "file": None, "status": None}

async def dummy(ws):
    header = {
	"apiName": "VTubeStudioPublicAPI",
	"apiVersion": "1.0",
	"requestID": "MyIDWithLessThan64Characters",
	"messageType": "APIStateRequest"
    }
    await ws.send(json.dumps(header))
    response = await ws.recv()
    response_data = json.loads(response)
    # emit_socketio_event("vts_debug", response_data)


def getModels():
    return VTS_MODELS