import json
from flask_socketio import SocketIO, emit
from app import app
import requests

socketio = SocketIO(app)
with open('/home/izitto/Desktop/Code/PAtDS/user_configs.json', 'r') as file:
    user_configs = json.load(file)
host = user_configs['DB']['host']
user = user_configs['DB']['user']
password = user_configs['DB']['password']
database = user_configs['DB']['database']

neko_timer = 0
derp_timer = 0

viewer = ""
friend = ""
# function to fetch user_configs.json
def fetch_user_configs():
    with open('/home/izitto/Desktop/Code/PAtDS/user_configs.json', 'r') as file:
        user_configs = json.load(file)
    return user_configs

# Socketio event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Function to emit Socketio events
def emit_socketio_event(event, data):
    socketio.emit(event, data)

# request below
def make_post_request(route, port, json_data):
    url = f"http://192.168.1.101:{port}/{route}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, data=json.dumps(json_data), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making POST request: {e}")
        return e

def make_get_request(route, port):
    url = f"http://192.168.1.101:{port}/{route}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")
        return e