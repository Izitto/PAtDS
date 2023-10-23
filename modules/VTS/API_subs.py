
import json
from modules.shared import emit_socketio_event, report_error

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

async def HotkeySub(ws):
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "EventSubscriptionRequest",
        "data": {
            "eventName": "HotkeyTriggeredEvent",
            "subscribe": True,
            "config": {
                "ignoreHotkeysTriggeredByAPI": False
            }
        }
    }
    await ws.send(json.dumps(header))

async def ModelMoveSub(ws):
    header = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "messageType": "EventSubscriptionRequest",
        "data": {
            "eventName": "ModelMovedEvent",
            "subscribe": True,
            "config": {
                
            }
        }
    }
    await ws.send(json.dumps(header))


