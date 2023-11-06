import modules.Control as Control
from app import app
import asyncio, threading
import atexit
import modules.VTS.vtstudio as vtstudio
import modules.TBOT.bot as bot

# Cleanup function
def cleanup():
    # Add any cleanup logic here
    # vtstudio.stop_vtstudio_connection()
    pass

# Register the cleanup function to be called on exit
atexit.register(cleanup)

# ###################################################
# if you don't understand, smoke crack first and try again
if __name__ == '__main__':
    # Start the Control logic
    Control.start()

    # Initiate the VTube Studio WebSocket connection and get the thread object
    vtstudio_thread = vtstudio.initiate_vtstudio_connection()
    
    # Start the Flask app
    app.run(debug=False, port=80, host='0.0.0.0')

    # Join the VTube Studio WebSocket thread
    vtstudio_thread.join()

    # Join the Control logic
    Control.join()




