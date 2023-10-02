from modules.shared import emit_socketio_event
import nmap
import time
import websocket


PLUGIN_NAME = "PAtDS"
DEVELOPER_NAME = "Izitto"
TOKEN_PATH = "/home/izitto/Desktop/Code/PAtDS/vts_token.txt"
VERSION = "1.0"

# New function to discover and connect to WebSocket API server
def discover_and_connect():
    ws_address = None
    while True:
        nm = nmap.PortScanner()
        nm.scan(hosts='192.168.0.0/24', arguments='-p 8001')  # Adjust the IP range if needed
        for host in nm.all_hosts():
            if nm[host]['tcp'][8001]['state'] == 'open':
                ws_address = f"ws://{host}:8001"
                break

        if ws_address:
            try:
                ws = websocket.create_connection(ws_address)
                # You can add any logic here after successfully connecting to the WebSocket server
                # For now, I'm just printing the connection status
                print(f"Connected to {ws_address}")
                while True:
                    # Check if the connection is still alive
                    if not ws.connected:
                        print("Connection lost. Rediscovering...")
                        break
                    time.sleep(5)
            except websocket.WebSocketException:
                print(f"Failed to connect to {ws_address}. Retrying...")
        else:
            print("WebSocket API server not found. Retrying in 5 seconds...")
        time.sleep(5)

# Start the discovery and connection process in a separate thread
# threading.Thread(target=discover_and_connect, daemon=True).start()