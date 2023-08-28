
from flask import Flask, request, render_template, current_app, jsonify
from flask_cors import CORS
app = Flask(__name__, template_folder='/home/izitto/Desktop/Code/PAtDS/templates', static_folder='/home/izitto/Desktop/Code/PAtDS/static', )
CORS(app)
app.config["SECRET_KEY"] = "secret!"

import json
import pymysql
import modules
from time import sleep
import queue





