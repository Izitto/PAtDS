import psutil
from flask import render_template, request, jsonify, send_from_directory, abort
import time
from datetime import timedelta
from app import app
import modules.shared as shared
import os

# route for system stats

@app.route('/stats', methods=['GET'])
def system_stats():
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    boot = psutil.boot_time()
    uptime_seconds = time.time() - boot
    uptime = timedelta(seconds = uptime_seconds)
    cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
    return render_template('sys_stats.html', cpu_usage=cpu_usage, mem_usage=mem_usage, disk_usage=disk_usage, uptime=uptime, cpu_temp=cpu_temp)