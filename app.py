import queue
from time import sleep
import modules
import pymysql
from flask import Flask, request, render_template, current_app, jsonify, session, redirect, url_for, flash, send_from_directory, send_file
from flask_cors import CORS
import logging
import os
app = Flask(__name__, template_folder='/home/izitto/Desktop/Code/PAtDS/templates',
            static_folder='/home/izitto/Desktop/Code/PAtDS/static', )


CORS(app)
app.config["SECRET_KEY"] = "secret!"