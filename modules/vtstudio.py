import json
from modules.shared import emit_socketio_event


class VTubeStudioAPI:

    def load_model(self, model_id):
        # Construct the request payload
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "LoadModelRequest",
            "data": {
                "modelID": model_id
            }
        }
        # Send the request (you might need to modify this based on your existing implementation)
        self.send_request(payload)

    def get_current_loaded_model_id(self):
        # Construct the request payload for getting the currently loaded model
        # (Based on the documentation, you might need to send a request and parse the response)

    def get_hotkey_list(self):
        # Construct the request payload for getting the list of hotkeys
        # (Similar to the above method)

    def trigger_hotkey(self, hotkey_id):
        # Construct the request payload for triggering a hotkey

    def get_expression_list(self):
        # Construct the request payload for getting the list of expressions

    def get_expression_state(self):
        # Construct the request payload for getting the current expression state

    def toggle_or_set_expression(self, expression_name, state):
        # Construct the request payload for toggling or setting an expression

    def subscribe_to_events(self):
        # Construct the request payload for subscribing to events
        # Use the EventSubscriptionRequest as mentioned in the documentation
        # You can subscribe to multiple events like ModelLoadedEvent, HotkeyTriggeredEvent, etc.
        # When an event is triggered, use the emit_socketio_event from shared.py to send a socket event
