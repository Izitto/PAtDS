from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests
import json
import os
from app import app
import modules.vtstudio as vtstudio

# pages
@app.route('/vts/home')
def twitch_home():
    return render_template('vts_manager/home.html')

# API ENDPOINTS /vts/api/...

