
import queue
from time import sleep
import modules
import pymysql
from flask import Flask, request, render_template, current_app, jsonify, session, redirect, url_for, flash, send_from_directory, send_file
from flask_cors import CORS
import bcrypt
import ipaddress
import hashlib
import json
app = Flask(__name__, template_folder='/home/izitto/Desktop/Code/PAtDS/templates',
            static_folder='/home/izitto/Desktop/Code/PAtDS/static', )
CORS(app)
app.config["SECRET_KEY"] = "secret!"


def is_local_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False

def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(encrypted_password):
    with open('/home/izitto/Desktop/Code/PAtDS/user_configs.json', 'r') as f:
        config = json.load(f)
    return encrypted_password == config['session']['password']

@app.before_request
def check_ip_and_password():
    if request.endpoint == 'password_prompt':
        return  # Skip the check for this route
    user_ip = request.remote_addr
    if not is_local_ip(user_ip):
        encrypted_password = session.get('encrypted_password')
        if encrypted_password is None or not verify_password(encrypted_password):
            return redirect(url_for('password_prompt'))
        else:
            return redirect(url_for('index'))

        
@app.route('/password_prompt', methods=['GET', 'POST'])
def password_prompt():
    if request.method == 'POST':
        encrypted_password = request.form['password']
        if verify_password(encrypted_password):
            session['encrypted_password'] = encrypted_password
            return redirect(url_for('index'))  # Redirect to some other route
        else:
            flash('Invalid password')
    return render_template('password_prompt.html')
