
# import modules.Control as Control
# import modules.VTS.vtstudio as vtstudio
# import modules.TBOT.bot as bot
from app import app
# start with gunicorn -c gunicorn_config.py run:app
# ###################################################
# if you don't understand, smoke crack first and try again

'''
#  test server, deprecated
if __name__ == '__main__':
    # Start the Control logic
    # Control.start()

    # Initiate the VTube Studio WebSocket connection and get the thread object
    # vtstudio_thread = vtstudio.initiate_vtstudio_connection()
    # tbot_thread = bot.initiate_tbot_connection()
    
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0')

    # Join the VTube Studio WebSocket thread
    # vtstudio_thread.join()
    # tbot_thread.join()

    # Join the Control logic
    # Control.join()

'''
'''
def init_app():
    
    # Start modules
    Control.start()
    vtstudio_thread = vtstudio.initiate_vtstudio_connection()
    tbot_thread = bot.initiate_tbot_connection()
    app = app
    # stop modules
    vtstudio_thread.join()
    tbot_thread.join()
    Control.join()
'''
# app = app
import eventlet
from eventlet import wsgi
# eventlet.monkey_patch(socket=True, select=True, time=True)
if __name__ == '__main__':
    wsgi.server(eventlet.listen(("0.0.0.0", 8000)), app)
    # app.run(debug=True, host='0.0.0.0', port=8000)

 



