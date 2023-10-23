import json
from flask import jsonify
from modules.VTS.objects import VTS_COORDS, VTS_MODELS, VTS_EXPRESSIONS, Model, Expression
import modules.VTS.API_requests as API_requests
from modules.VTS.send_queue import sender
from modules.shared import emit_socketio_event, report_error
TOKEN_PATH = "/home/izitto/Desktop/Code/PAtDS/vts_token.txt"

async def Listen(response):
    # response = await ws.recv()
    response_data= json.loads(response)
    # ModelLoadedEvent
    try:
        # ModelLoadedEvent
        if response_data.get('messageType', str()) == "ModelLoadedEvent":
            emit_socketio_event("vts_event_log", "model changed")
            VTS_MODELS.setModelSatus(response_data.get('data', {}).get('modelID', []), response_data.get('data', {}).get('modelLoaded', []))
            emit_socketio_event("vts_data_models", VTS_MODELS.toJSON())
            await sender(API_requests.fetch_vts_expressions, None)
            emit_socketio_event("vts_event_log1", "api events: " + str(response_data))

        # HotkeyTriggeredEvent
        elif response_data.get('messageType', str()) == "HotkeyTriggeredEvent":
            emit_socketio_event("vts_event_log", "hotkey triggered")
            VTS_EXPRESSIONS.setExpressionStatus(response_data.get('data', {}).get('expressionName', []), response_data.get('data', {}).get('active', []))
            emit_socketio_event("vts_data_expressions", VTS_EXPRESSIONS.toJSON())
            emit_socketio_event("vts_event_log", "api events: " + str(response_data))


        # ModelMovedEvent
        elif response_data.get('messageType', str()) == "ModelMovedEvent":
            VTS_COORDS.setCoords(response_data.get('data', {}).get('modelPosition', []).get('positionX', []), response_data.get('data', {}).get('modelPosition', []).get('positionY', []), response_data.get('data', {}).get('modelPosition', []).get('size', []), response_data.get('data', {}).get('modelPosition', []).get('rotation', []))
            emit_socketio_event("vts_data_coords", VTS_COORDS.toJSON())
            emit_socketio_event("vts_event_log", "model moved")
            emit_socketio_event("vts_event_log", "api events: " + str(response_data))


        # AuthenticationTokenResponse
        elif response_data.get('messageType', str()) == "AuthenticationTokenResponse":
            # If a token is received from the server, store it in the text file
            if response_data.get('data', {}).get('authenticationToken'):
                token = response_data['data']['authenticationToken']
                with open(TOKEN_PATH, 'w') as token_file:
                    token_file.write(token)
                emit_socketio_event("vts_event_log", "api request: " + str(response_data))
                await sender(API_requests.authenticate_with_server, None)
            else:
                emit_socketio_event("vts_event_log", "No token received from server")
                emit_socketio_event("vts_event_log", "api request: " + str(response_data))
        
        # AuthenticationResponse
        elif response_data.get('messageType', str()) == "AuthenticationResponse":
            if response_data.get('data', {}).get('authenticated') is True:
                emit_socketio_event("vts_event_log", "Authenticated with VTube Studio")
            else:
                emit_socketio_event("vts_event_log", "Authentication with VTube Studio failed")
                emit_socketio_event("vts_event_log", response_data)
        
        # AvailableModelsResponse
        elif response_data.get('messageType', str()) == "AvailableModelsResponse":
            VTS_MODELS.addModels([Model(model["modelName"], model["modelID"], model["modelLoaded"]) for model in response_data.get('data', {}).get('availableModels', [])])
            emit_socketio_event("vts_data_models", VTS_MODELS.toJSON())
            emit_socketio_event("vts_event_log", "api request: " + str(response_data))

        # ExpressionStateResponse
        elif response_data.get('messageType', str()) == "ExpressionStateResponse":
            VTS_EXPRESSIONS.addExpressions([Expression(expression["name"], expression["file"], expression["active"]) for expression in response_data.get('data', {}).get('expressions', [])])
            emit_socketio_event("vts_data_expressions", VTS_EXPRESSIONS.toJSON())
            emit_socketio_event("vts_event_log", "api request: " + str(response_data))
        
        # ExpressionActivationResponse
        elif response_data.get('messageType', str()) == "ExpressionActivationResponse":
            await sender(API_requests.fetch_vts_expressions, None)
            emit_socketio_event("vts_event_log", "api request: " + str(response_data))

        
        


    except Exception as e:
        report_error("vts_event_bug")
        emit_socketio_event("vts_event_bug", "api request: " + str(e))