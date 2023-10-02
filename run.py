import modules.Control as Control, modules.vtstudio as vtstudio
from app import app
import asyncio, threading
from modules import vtstudio
import atexit
import modules.vtstudio as vtstudio

# Cleanup function
def cleanup():
    # Add any cleanup logic here
    vtstudio.stop_vtstudio_connection()

# Register the cleanup function to be called on exit
atexit.register(cleanup)

# ###################################################
# if you don't understand, smoke crack first and try again
if __name__ == '__main__':
    # Start the Control logic
    Control.start()

    vtstudio.start_websocket_connection()
    
    # Start the Flask app
    app.run(debug=False, port=80, host='0.0.0.0')
    # Join the Control logic
    Control.join()
