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
IS_CONNECTED = False
IS_AUTH = False
from modules.VTS.send_queue import sender


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


async def fetch_vts_models(ws):
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "AvailableModelsRequest"
    }
    await ws.send(json.dumps(header))


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
    await ws.send(json.dumps(header))

async def loadModel(ws, model_id):
    # global req_model_id
    emit_socketio_event("vts_req_log", "model requested: " + model_id)
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "ModelLoadRequest",
        "data": {
            "modelID": model_id
        }
    }
    await ws.send(json.dumps(header))

async def setExpression(ws, expression):
    # global req_expression
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "ExpressionActivationRequest",
        "data": {
            "expressionFile": expression['file'],
            "active": expression['status']
        }
    }
    await ws.send(json.dumps(header))


async def moveModel(ws, model_id, position):
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "MoveModelRequest",
        "data": {
            "modelID": model_id,
            "timeInSeconds": position['timeInSeconds'],
            "valuesAreRelativeToModel": position['valuesAreRelativeToModel'],
            "positionX": position['positionX'],
            "positionY": position['positionY'],
            "rotation": position['rotation'],
            "size": position['size']
        }
    }
    await ws.send(json.dumps(header))