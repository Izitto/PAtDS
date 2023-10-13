from modules.shared import emit_socketio_event
import websockets, asyncio, threading, queue
from modules.VTS.discover_server import discover_vtube_studio_server, SERVER_IP, SERVER_PORT
from modules.VTS.API_requests import authenticate_with_server, req_model_id, req_expression, req_hotkeyID, models_fetched, expressions_fetched, VTS_MODELS, VTS_EXPRESSIONS, send
# receive = queue.Queue()


ws = websockets
# function variables




async def start_websocket_connection(send):
    global SERVER_IP, SERVER_PORT, IS_AUTH, IS_CONNECTED, VTS_MODELS, VTS_EXPRESSIONS
    while True:
        
        if not SERVER_IP or not SERVER_PORT:
            emit_socketio_event("vts_debug", "Discovering VTube Studio API Server...")
            discover_vtube_studio_server()
        
        if SERVER_IP and SERVER_PORT:
            uri = f"ws://{SERVER_IP}:{SERVER_PORT}"
            # emit_socketio_event("vts_debug", f"Connecting to VTube Studio API Server at {uri}...")
            try:
                emit_socketio_event("vts_debug", f"Connecting to VTube Studio API Server at {uri}...")
                async with websockets.connect(uri) as ws:
                    # queue for calling functions from API_requests module
                    response = send.get_nowait()
                    
            
            except websockets.ConnectionClosed:
                emit_socketio_event("vts_debug", "Connection closed")
                IS_AUTH = False
                IS_CONNECTED = False
                SERVER_IP, SERVER_PORT = "", None  # Reset IP and port to trigger rediscovery
            except Exception as e:
                emit_socketio_event("vts_debug", f"Error: {e} {type(e)} {e.args} {e.__traceback__.tb_lineno}")
                IS_AUTH = False
                IS_CONNECTED = False
                await asyncio.sleep(5)  # Wait for 5 seconds before retrying
                

# Call the function
def initiate_vtstudio_connection():
    try:
        def run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(start_websocket_connection())

        thread = threading.Thread(target=run, args=(send,))
        thread.daemon = True
        thread.start()
        return thread
    except Exception as e:
        print(f"Error: {e} {type(e)} {e.args} {e.__traceback__.tb_lineno}")
        return None



