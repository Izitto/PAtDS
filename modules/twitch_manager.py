from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests
import json
import os
from app import app

# Load Twitch Configurations

twitch_configs = {}
try:
    with open("/home/izitto/Documents/Code/PAtDS/twitch_configs.json", "r") as f:
        content = f.read().strip()  # Remove leading/trailing whitespace
        if content:  # Check if the file is empty
            twitch_configs = json.loads(content)
except json.JSONDecodeError:
    print("JSON Decode Error: The file is not a valid JSON. Using default settings.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Twitch Pages


@app.route('/twitch/home')
def twitch_home():
    return render_template('twitch_manager/home.html')


@app.route('/twitch/redeems')
def twitch_redeems():
    return render_template('twitch_manager/redeems.html')
