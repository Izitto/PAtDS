import json
from modules.VTS.objects import VTS_MODELS, VTS_EXPRESSIONS, Model, Expression
from modules.shared import emit_socketio_event


async def Listen(response):
    # response = await ws.recv()
    response_data= json.loads(response)
    if response_data.get('messageType', str()) == "ModelLoadedEvent":
        emit_socketio_event("vts_debug", "model changed")
        VTS_MODELS.setModelSatus(response_data.get('data', {}).get('modelID', []), response_data.get('data', {}).get('modelLoaded', []))
        emit_socketio_event("vts_debug", "api events: " + str(response_data))

    elif response_data.get('messageType', str()) == "HotkeyTriggeredEvent":
        emit_socketio_event("vts_debug", "hotkey triggered")
        Expression.setState(response_data.get('data', {}).get('expressionFile', []), response_data.get('data', {}).get('active', []))
        