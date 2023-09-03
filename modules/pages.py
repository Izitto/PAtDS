from flask import render_template, request
from app import app
import modules.Control as Control
import os
control_system = Control.ControlSystem()

#      main routes for the web app
@app.route("/")
def index():
    return render_template('index.html')


# Mapping from button names to command_map keys
button_to_command = {
    "A1": "HDMI_A1",
    "A2": "HDMI_A2",
    "A3": "HDMI_A3",
    "A4": "HDMI_A4",
    "Boot Main PC": "start_main",
    "B1": "HDMI_B1",
    "B2": "HDMI_B2",
    "B3": "HDMI_B3",
    "B4": "HDMI_B4",
    "Switch USB": "switch_usb",
    "Restart Service": "restart_service",  # Update this if you have a corresponding command
    "Reboot Device": "reboot"
}
@app.route('/control', methods=['GET', 'POST'])
def patds():
    if request.method == 'POST':
        button = request.form['button']
        command = button_to_command.get(button, None)
        if command:
            control_system.execute_command(command)
    return render_template('patds.html', methods = ['GET', 'POST', 'DELETE'])

@app.route('/thumbnailmaker', methods=['GET', 'POST'])
def thumbnailmaker():
    return render_template('make_thumbnail.html', methods = ['GET', 'POST', 'DELETE'])



@app.route('/logs', methods=['GET', 'POST'])
def logs():
    return render_template('log.html', methods = ['GET', 'POST', 'DELETE'])