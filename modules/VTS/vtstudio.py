from modules.shared import emit_socketio_event
import websockets, asyncio, threading, queue
from modules.VTS.discover_server import discover_vtube_studio_server, SERVER_IP, SERVER_PORT
from modules.VTS.API_requests import authenticate_with_server, VTS_MODELS, VTS_EXPRESSIONS, send, IS_CONNECTED, IS_AUTH
from modules.VTS.API_requests import fetch_vts_models, fetch_vts_expressions
# receive = queue.Queue()

ws = websockets
# function variables

send.put_nowait(authenticate_with_server(ws))
send.put_nowait(fetch_vts_models(ws))
send.put_nowait(fetch_vts_expressions(ws))

async def start_websocket_connection(send):
    global SERVER_IP, SERVER_PORT, VTS_MODELS, VTS_EXPRESSIONS, IS_CONNECTED, IS_AUTH
    send = send
    while True:
        
        if not SERVER_IP or not SERVER_PORT:
            emit_socketio_event("vts_debug", "IP: " + str(SERVER_IP) + " PORT: " + str(SERVER_PORT) + " Discovering VTube Studio API Server...)")
            emit_socketio_event("vts_debug", "Discovering VTube Studio API Server...")
            SERVER_IP, SERVER_PORT = discover_vtube_studio_server()
        
        if SERVER_IP or SERVER_PORT:
            uri = f"ws://{SERVER_IP}:{SERVER_PORT}"
            # emit_socketio_event("vts_debug", f"Connecting to VTube Studio API Server at {uri}...")
            try:
                # emit_socketio_event("vts_debug", f"Connecting to VTube Studio API Server at {uri}...")
                async with websockets.connect(uri) as ws:
                    # queue for calling functions from API_requests module
                    '''if await getAuth() == False:
                        # IS_CONNECTED = True
                        # IS_AUTH = await authenticate_with_server(ws)
                        await setAuth(await authenticate_with_server(ws))
                        emit_socketio_event("vts_debug", "Connected to VTube Studio API Server")
                    '''
                    await send.get_nowait()
                    
                    
            
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
        def run(send):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(start_websocket_connection(send))

        thread = threading.Thread(target=run, args=(send,))
        thread.daemon = True
        thread.start()
        return thread
    except Exception as e:
        print(f"Error: {e} {type(e)} {e.args} {e.__traceback__.tb_lineno}")
        return None



