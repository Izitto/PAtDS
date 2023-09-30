import json
import socket
import websockets
import asyncio
from modules.shared import emit_socketio_event
import os

APP_NAME = "PAtDS"
DEVELOPER_NAME = "Izitto"
BASE_URL = "ws://192.168.0.101:8001"
VTS_TOKEN_PATH = "/home/izitto/Desktop/Code/PAtDS/vts_token.txt"

