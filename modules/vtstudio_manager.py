from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests
import json
import os
from app import app
import modules.vtstudio as vtstudio

# pages
@app.route('/vts/home')
def twitch_home():
    # Fetch available models (assuming you have a function get_available_models in vtstudio.py)
    models = vtstudio.get_available_models()
    return render_template('vts_manager/home.html', models=models)


# API ENDPOINTS /vts/api/...

