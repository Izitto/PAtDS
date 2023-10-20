
import json
from modules.shared import emit_socketio_event


async def ModelSub(ws):
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "EventSubscriptionRequest",
        "data": {
            "eventName": "ModelLoadedEvent",
            "subscribe": True,
            "config": {
                
            }
        }
    }
    await ws.send(json.dumps(header))
    response = await ws.recv()
    response_data = json.loads(response)
    emit_socketio_event("vts_debug", "model sub response: " + str(response_data))

async def HotkeySub(ws):
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "EventSubscriptionRequest",
        "data": {
            "eventName": "HotkeyTriggeredEvent",
            "subscribe": True,
            "config": {
                "onlyForAction": "ToggleExpression",
                "ignoreHotkeysTriggeredByAPI": False
            }
        }
    }
    await ws.send(json.dumps(header))
    response = await ws.recv()
    response_data = json.loads(response)
    emit_socketio_event("vts_debug", "hotkey sub response: " + str(response_data))