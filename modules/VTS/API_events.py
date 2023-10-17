import json, queue
from modules.shared import emit_socketio_event

async def ModelEvent(ws):
    header = {
        "eventName": "ModelLoadedEvent"
    }
    await ws.send(json.dumps(header))
    response = await ws.recv()
    response_data = json.loads(response)
    emit_socketio_event("vts_debug", Str(response_data))