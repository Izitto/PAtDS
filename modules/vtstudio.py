import json
import socket
import websockets
from modules.shared import emit_socketio_event
import os

# BASE_URL = "ws://192.168.0.101:8001"
BASE_URL = ""
VTS_TOKEN_PATH = "/home/izitto/Desktop/Code/PAtDS/vts_token.txt"

async def search_api_server():
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.settimeout(5)
        try:
            # Send a broadcast message
            s.sendto(b'VTubeStudio', ('<broadcast>', 8001))
            # Receive response
            data, addr = s.recvfrom(1024)
            global BASE_URL
            BASE_URL = f"ws://{addr[0]}:8001"
            emit_socketio_event('vtstudio_api_server', {'address': BASE_URL})
        except socket.timeout:
            emit_socketio_event('vtstudio_error', {'message': 'No response from VTubeStudio API server'})

async def get_available_models():
    if not BASE_URL:
        emit_socketio_event('vtstudio_error', {'message': 'API server address not set'})
        return

    async with websockets.connect(BASE_URL) as ws:
        # Authenticate with the API
        with open(VTS_TOKEN_PATH, 'r') as f:
            token = f.read().strip()
        auth_data = {
            "type": "AuthenticationRequest",
            "APIAuthenticationToken": token
        }
        await ws.send(json.dumps(auth_data))
        response = await ws.recv()
        response_data = json.loads(response)
        if response_data.get('authenticated'):
            # Request available models
            await ws.send(json.dumps({"type": "AvailableModelsRequest"}))
            models_response = await ws.recv()
            models_data = json.loads(models_response)
            emit_socketio_event('vtstudio_available_models', models_data)
        else:
            emit_socketio_event('vtstudio_error', {'message': 'Authentication failed'})

async def get_model_icons():
    if not BASE_URL:
        emit_socketio_event('vtstudio_error', {'message': 'API server address not set'})
        return

    async with websockets.connect(BASE_URL) as ws:
        # Authenticate with the API
        with open(VTS_TOKEN_PATH, 'r') as f:
            token = f.read().strip()
        auth_data = {
            "type": "AuthenticationRequest",
            "APIAuthenticationToken": token
        }
        await ws.send(json.dumps(auth_data))
        response = await ws.recv()
        response_data = json.loads(response)
        if response_data.get('authenticated'):
            # Request model icons
            await ws.send(json.dumps({"type": "ModelIconRequest"}))
            icons_response = await ws.recv()
            icons_data = json.loads(icons_response)
            emit_socketio_event('vtstudio_model_icons', icons_data)
        else:
            emit_socketio_event('vtstudio_error', {'message': 'Authentication failed'})
