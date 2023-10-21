import json
from modules.VTS.objects import VTS_MODELS, VTS_EXPRESSIONS, Model, Expression
import modules.VTS.API_requests as API_requests
from modules.VTS.send_queue import sender
from modules.shared import emit_socketio_event


async def Listen(response):
    # response = await ws.recv()
    response_data= json.loads(response)
    if response_data.get('messageType', str()) == "ModelLoadedEvent":
        emit_socketio_event("vts_event_log", "model changed")
        VTS_MODELS.setModelSatus(response_data.get('data', {}).get('modelID', []), response_data.get('data', {}).get('modelLoaded', []))
        await sender(API_requests.fetch_vts_expressions, None)
        emit_socketio_event("vts_event_log", "api events: " + str(response_data))

    elif response_data.get('messageType', str()) == "HotkeyTriggeredEvent":
        emit_socketio_event("vts_event_log", "hotkey triggered")
        VTS_EXPRESSIONS.setExpressionStatus(response_data.get('data', {}).get('expressionName', []), response_data.get('data', {}).get('active', []))
    
        