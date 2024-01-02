from app import app
import modules.Control as Control
import modules.VTS.vtstudio as vtstudio
import modules.TBOT.bot as bot

# start with gunicorn -c gunicorn_config.py run:app
# ###################################################
# if you don't understand, smoke crack first and try again

'''
test server, deprecated
if __name__ == '__main__':
    # Start the Control logic
    Control.start()

    # Initiate the VTube Studio WebSocket connection and get the thread object
    vtstudio_thread = vtstudio.initiate_vtstudio_connection()
    tbot_thread = bot.initiate_tbot_connection()
    
    # Start the Flask app
    app.run(debug=False, port=5000, host='0.0.0.0')

    # Join the VTube Studio WebSocket thread
    vtstudio_thread.join()
    tbot_thread.join()

    # Join the Control logic
    Control.join()

'''
def init_app():
    # Start the Control logic
    Control.start()
    vtstudio_thread = vtstudio.initiate_vtstudio_connection()
    tbot_thread = bot.initiate_tbot_connection()

    # Join the VTube Studio WebSocket thread
    vtstudio_thread.join()
    tbot_thread.join()
    Control.join()

