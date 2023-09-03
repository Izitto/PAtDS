'''
import modules.Control as Control
from app import app
# ###################################################
# if you don't understand, smoke crack first and try again
if __name__ == '__main__':
    Control.start()
    app.run(debug=False, port=80, host='0.0.0.0')
    Control.join()

'''
import modules.Control as Control
from app import app
import threading

if __name__ == '__main__':
    control_system = Control.ControlSystem()
    con = threading.Thread(target=Control.thread_control, args=(control_system,))
    con.start()
    app.run(debug=False, port=80, host='0.0.0.0')
    con.join()
