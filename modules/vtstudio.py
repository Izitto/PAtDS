import json
from modules.shared import emit_socketio_event
import requests

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
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "APIStateRequest"
        }
        response = self.send_request(payload)
        return response.get('data', {}).get('currentModelID')
    
    def get_all_model_icons(self):
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "AllModelIconRequest"
        }
        response = self.send_request(payload)
        return response.get('data', {}).get('modelIcons')
    

    
    def get_current_model_icon(self):
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "CurrentModelIconRequest"
        }
        response = self.send_request(payload)
        return response.get('data', {}).get('modelIcon')



    def get_hotkey_list(self):
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "HotkeysRequest"
        }
        response = self.send_request(payload)
        return response.get('data', {}).get('hotkeys')

    def trigger_hotkey(self, hotkey_id):
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "HotkeyTriggerRequest",
            "data": {
                "hotkeyID": hotkey_id
            }
        }
        self.send_request(payload)

    def get_expression_list(self):
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "AvailableExpressionsRequest"
        }
        response = self.send_request(payload)
        return response.get('data', {}).get('availableExpressions')

    def get_expression_state(self):
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "ExpressionStateRequest"
        }
        response = self.send_request(payload)
        return response.get('data', {}).get('currentExpression')

    def toggle_or_set_expression(self, expression_name, state):
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "ExpressionToggleRequest",
            "data": {
                "expressionName": expression_name,
                "expressionState": state
            }
        }
        self.send_request(payload)

    def subscribe_to_events(self):
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "EventSubscriptionRequest",
            "data": {
                "events": [
                    "ModelLoadedEvent",
                    "HotkeyTriggeredEvent",
                    "ExpressionChangedEvent"
                ]
            }
        }
        self.send_request(payload)

    def handle_event(self, event_data):
        # Parse the event_data to determine the type of event
        event_type = event_data.get("messageType")
        
        if event_type == "ModelLoadedEvent":
            model_id = event_data.get('data', {}).get('modelID')
            emit_socketio_event("model_loaded", {"modelID": model_id})
            
        elif event_type == "HotkeyTriggeredEvent":
            hotkey_id = event_data.get('data', {}).get('hotkeyID')
            emit_socketio_event("hotkey_triggered", {"hotkeyID": hotkey_id})
            
        elif event_type == "ExpressionChangedEvent":
            expression_name = event_data.get('data', {}).get('expressionName')
            expression_state = event_data.get('data', {}).get('expressionState')
            emit_socketio_event("expression_changed", {
                "expressionName": expression_name,
                "expressionState": expression_state
            })
            
        # You can add more event handlers as needed based on the VTube Studio API documentation
