
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
    try:
        await ws.send(json.dumps(header))
        response = await ws.recv()
        response_data = json.loads(response)
        emit_socketio_event("vts_sub_log", "model sub response: " + str(response_data))
    except Exception as e:
        report_error("vts_sub_bug")
        emit_socketio_event("vts_sub_bug", "model sub response: " + str(e))

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
    try:    
        await ws.send(json.dumps(header))
        response = await ws.recv()
        response_data = json.loads(response)
        emit_socketio_event("vts_sub_log", "hotkey sub response: " + str(response_data))
    except Exception as e:
        report_error("vts_sub_bug")
        emit_socketio_event("vts_sub_bug", "hotkey sub response: " + str(e))
