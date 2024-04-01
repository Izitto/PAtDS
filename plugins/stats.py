import psutil
import time
from datetime import timedelta
from threading import Event
import queue

def get_stats():
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    boot = psutil.boot_time()
    uptime_seconds = time.time() - boot
    uptime = timedelta(seconds = uptime_seconds)
    cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
    return {'cpu_usage': cpu_usage, 'mem_usage': mem_usage, 'disk_usage': disk_usage, 'uptime': uptime, 'cpu_temp': cpu_temp}

def run(stop_event: Event, queue: queue.Queue):
    while not stop_event.is_set():
        stats = get_stats()
        time.sleep(1)


