'''
import atexit
import modules.Control as Control
import modules.VTS.vtstudio as vtstudio
import modules.TBOT.bot as bot
from threading import Thread, Event
stop_control = Event()
controlThread = None

def start():
    global controlThread
    if controlThread is not None:
        print("Control thread already running")
        return
    controlThread = Thread(target=Control.thread_control, args=(stop_control,))
    controlThread.start()

def kill(): # stops the control thread and joins it
    global controlThread
    if controlThread is None:
        print("Control thread not running")
        return
    stop_control.set()
    controlThread.join()
    controlThread = None


def status():
    global controlThread
    if controlThread is None:
        return False
    return controlThread.is_alive()

def exit_handler():
    if controlThread is None and not controlThread.is_alive():
        print("Control thread not running")
        return
    stop_control.set()
    controlThread.join()
    print("Exiting...")

atexit.register(exit_handler)
'''

"""
import atexit
import modules.Control as Control
import modules.VTS.vtstudio as vtstudio

Control.start()
vtstudio_thread = vtstudio.initiate_vtstudio_connection()

def exit_handler():
    Control.join()
    vtstudio_thread.join()


atexit.register(exit_handler)
"""

import atexit
import eventlet
import modules.Control as Control
import modules.VTS.vtstudio as vtstudio

# Assuming Control.start() is adapted for Eventlet if needed
Control.start()

# This now returns a GreenThread object from Eventlet
vtstudio_thread = vtstudio.initiate_vtstudio_connection()

def exit_handler():
    # For Control, ensure a proper shutdown or wait mechanism is implemented
    # This is a placeholder; your actual implementation may vary
    Control.shutdown()  # Assuming you implement a shutdown method

    # Wait for the green thread to complete
    vtstudio_thread.shutdown()

atexit.register(exit_handler)
