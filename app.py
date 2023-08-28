
import queue
from time import sleep
import modules
import pymysql
from flask import Flask, request, render_template, current_app, jsonify, session, redirect, url_for, flash, send_from_directory, send_file
from flask_cors import CORS
import bcrypt
import json
app = Flask(__name__, template_folder='/home/izitto/Desktop/Code/PAtDS/templates',
            static_folder='/home/izitto/Desktop/Code/PAtDS/static', )
CORS(app)
app.config["SECRET_KEY"] = "secret!"


def is_local_ip(ip_address):
    return ip_address.startswith("192.168.")

def verify_password(entered_password):
    with open("/home/izitto/Desktop/Code/PAtDS/user_configs.json", "r") as f:
        config = json.load(f)
    hashed_password = config.get("password").encode('utf-8')
    return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password)

@app.route('/verify_password', methods=['POST'])
def verify_password_route():
    password = request.form.get('password')
    ip_address = request.remote_addr
    if verify_password(password):
        session['ip_address'] = ip_address
        flash('Password is correct!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Password is incorrect!', 'error')
        return redirect(url_for('password_prompt'))

@app.route('/password_prompt')
def password_prompt():
    return render_template('password_prompt.html')

@app.before_request
def before_request():
    ip_address = request.remote_addr
    if not is_local_ip(ip_address):
        if 'ip_address' not in session or session['ip_address'] != ip_address:
            if request.endpoint not in ['password_prompt', 'verify_password']:
                return redirect(url_for('password_prompt'))