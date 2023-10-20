from modules.shared import emit_socketio_event, report_error
import websockets, asyncio, threading, queue
from modules.VTS.discover_server import discover_vtube_studio_server, SERVER_IP, SERVER_PORT
from modules.VTS.API_requests import VTS_MODELS, VTS_EXPRESSIONS, send, IS_CONNECTED, IS_AUTH
import modules.VTS.API_requests as API_requests
import modules.VTS.API_subs as API_subs
import modules.VTS.API_events as API_events
import sys
import os
from time import sleep
# function variables
# queue setup { function, args}
async def setup():
    await sender(API_requests.authenticate_with_server, None)
    await sender(API_requests.fetch_vts_models, None)
    await sender(API_requests.fetch_vts_expressions, None)
    await sender(API_subs.ModelSub, None)

    

async def sender(function, args):
    send.put_nowait( (function, args) )

async def start_websocket_connection(send):
    await setup()
    global VTS_EXPRESSIONS, IS_CONNECTED, IS_AUTH
    SERVER_IP, SERVER_PORT = "", None
    while True:
        
        if SERVER_IP == "" or SERVER_PORT is None:
            emit_socketio_event("vts_debug", "Discovering VTube Studio API Server...")
            SERVER_IP, SERVER_PORT = discover_vtube_studio_server()
            emit_socketio_event("vts_debug", "IP: " + str(SERVER_IP) + " PORT: " + str(SERVER_PORT) + " Attempting to connect...")
        
        if SERVER_IP != "" or SERVER_PORT is not None:
            uri = f"ws://{SERVER_IP}:{SERVER_PORT}"
            try:
                async with websockets.connect(uri) as ws:
                    while True:  # Infinite loop to keep the connection alive
                        while not send.empty():
                            list = send.get_nowait()
                            func_to_call, arg = list[0], list[1]
                            emit_socketio_event("vts_debug1", f"Calling {func_to_call.__name__} with arg {arg}")
                            if arg is not None:
                                await func_to_call(ws, arg)
                            else:
                                await func_to_call(ws)
                        else:
                            response = await ws.recv()
                            emit_socketio_event("vts_debug2", f"Received: {response}")
                            if response is None:
                                break
                            await API_events.Listen(response)
                        if ws.closed:
                            break

                    
                    
                    
            except websockets.InvalidStatusCode as e:
                report_error("vts_error")
                IS_AUTH = False
                IS_CONNECTED = False
                await setup()
                SERVER_IP, SERVER_PORT = "", None
            except websockets.ConnectionClosed:
                report_error("vts_error")
                IS_AUTH = False
                IS_CONNECTED = False
                SERVER_IP, SERVER_PORT = "", None  # Reset IP and port to trigger rediscovery
                await setup()
            except Exception as e:
                report_error("vts_error")
                IS_AUTH = False
                IS_CONNECTED = False
                await setup()
                SERVER_IP, SERVER_PORT = "", None  # Reset IP and port to trigger rediscovery
                await asyncio.sleep(5)  # Wait for 5 seconds before retrying
        

# Call the function
def initiate_vtstudio_connection():
    try:
        def run(send):
            sleep(5)
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

'''

async def start_websocket_connection():
    global ws
    try:
        ws = await websockets.connect(f"ws://192.168.0.101:8001")
        await authenticate_with_server(ws)
    except Exception as e:
        emit_socketio_event("vts_debug", f"Error: {e} {type(e)} {e.args} {e.__traceback__.tb_lineno}")
    while True:
        pass

asyncio.set_event_loop(asyncio.new_event_loop().run_until_complete(start_websocket_connection()))
'''