
import queue
from time import sleep
import modules
import pymysql
from flask import Flask, request, render_template, current_app, jsonify, session, redirect, url_for, flash, send_from_directory, send_file
from flask_cors import CORS
import logging
import os
from flask_webpack import Webpack
app = Flask(__name__, template_folder='/home/izitto/Desktop/Code/PAtDS/templates',
            static_folder='/home/izitto/Desktop/Code/PAtDS/static', )

Webpack = Webpack()
params = {
        'DEBUG': True,
        'WEBPACK_MANIFEST_PATH': '/home/izitto/Desktop/Code/PAtDS/build/manifest.json'
    }
CORS(app)
app.config["SECRET_KEY"] = "secret!"
app.config.update(params)
Webpack.init_app(app)
# Create logs directory if it doesn't exist
log_dir = os.path.join(app.static_folder, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Dynamically create log files for each module
module_names = ["Control", "api", "pages", "twitch_manager", "overlay_manager", "shared"]  # List of module names in /modules
for module_name in module_names:
    log_file_path = os.path.join(log_dir, f"{module_name}.txt")
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file_path)
    logger.addHandler(file_handler)

# Now you can use these loggers in your modules to log information
# For example, in Control.py, you can use logging.getLogger("Control").info("Some log message")