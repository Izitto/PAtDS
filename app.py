import queue
import atexit
from time import sleep

import pymysql
import flask_socketio
from flask import Flask, request, render_template, current_app, jsonify, session, redirect, url_for, flash, send_from_directory, send_file
from flask_cors import CORS
import logging
import os

app = Flask(__name__, template_folder='/home/izitto/Desktop/Code/PAtDS/templates',
            static_folder='/home/izitto/Desktop/Code/PAtDS/static', )

socketio = flask_socketio.SocketIO(app, cors_allowed_origins="*")
CORS(app)
app.config["SECRET_KEY"] = "secret!"
import modules


