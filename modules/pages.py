from flask import render_template, request
from app import app
import modules.Control as Control
import os


#      main routes for the web app
@app.route("/")
def index():
    return render_template('index.html')
@app.route('/control', methods=['GET', 'POST'])
def patds():
    if request.method == 'POST':
        if request.form['button'] == 'Switch USB':
            Control.commands("switch_usb")
        if request.form['button'] == 'Boot Main PC':
            Control.commands("start_main")
        if request.form['button'] == 'Boot Game PC':
            Control.commands("start_game")
        if request.form['button'] == 'A1':
            Control.commands("HDMI_A1")
        if request.form['button'] == 'A2':
            Control.commands("HDMI_A2")
        if request.form['button'] == 'A3':
            Control.commands("HDMI_A3")
        if request.form['button'] == 'A4':
            Control.commands("HDMI_A4")
        if request.form['button'] == 'B1':
            Control.commands("HDMI_B1")
        if request.form['button'] == 'B2':
            Control.commands("HDMI_B2")
        if request.form['button'] == 'B3':
            Control.commands("HDMI_B3")
        if request.form['button'] == 'B4':
            Control.commands("HDMI_B4")
        if request.form['button'] == 'Restart Service':
            os.system("sudo systemctl restart PatDS.service")
        if request.form['button'] == 'Reboot Device':
            os.system("sudo reboot")

    return render_template('patds.html', methods = ['GET', 'POST', 'DELETE'])

@app.route('/thumbnailmaker', methods=['GET', 'POST'])
def thumbnailmaker():
    return render_template('make_thumbnail.html', methods = ['GET', 'POST', 'DELETE'])



@app.route('/logs', methods=['GET', 'POST'])
def logs():
    return render_template('log.html', methods = ['GET', 'POST', 'DELETE'])