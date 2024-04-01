import plugins
import threading
import time
import os
from threading import Event
from modules.shared import emit_socketio_event as emit_socketio_event

stats = plugins.stats.run

def create_thread(func):
    # create a thread for a given function
    stop_event = Event()
    thread = threading.Thread(target=func, args=(stop_event,))
    thread.start()
    return thread, stop_event

def stop_thread(thread, stop_event):
    # stop a thread
    stop_event.set()
    thread.join()

