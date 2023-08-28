
import queue
from time import sleep
import modules
import pymysql
from flask import Flask, request, render_template, current_app, jsonify, session, redirect, url_for, flash, send_from_directory, send_file
from flask_cors import CORS
import bcrypt
import json
from Crypto.Cipher import AES
from base64 import b64decode
app = Flask(__name__, template_folder='/home/izitto/Desktop/Code/PAtDS/templates',
            static_folder='/home/izitto/Desktop/Code/PAtDS/static', )
CORS(app)
app.config["SECRET_KEY"] = "secret!"


@app.before_request
def check_local():
    if request.endpoint == 'password_prompt':
        return
    user_ip = request.remote_addr
    if not user_ip.startswith("192.168."):  # Assuming local IPs start with 192.168.
        if 'authenticated' not in session:
            return redirect(url_for('password_prompt'))

@app.route('/password_prompt', methods=['GET', 'POST'])
def password_prompt():
    if request.method == 'POST':
        encrypted_password = request.json.get('password')
        cipher = AES.new('secret-key', AES.MODE_CBC, iv=b64decode(encrypted_password)[:16])
        decrypted_password = cipher.decrypt(b64decode(encrypted_password)[16:]).rstrip(b"\0").decode('utf-8')
        password = decrypted_password
        with open('/home/izitto/Desktop/Code/PAtDS/user_configs.json', 'r') as f:
            data = json.load(f)
            stored_password = data['session']['password']
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            session['authenticated'] = True
            return redirect(url_for('index'))  # Assuming 'index' is the main route
        else:
            flash('Incorrect password')
    return render_template('password_prompt.html')