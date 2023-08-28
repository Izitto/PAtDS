from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests
import json
import os
import shared
from app import app

# Load Twitch Configurations
try:
    with open("/home/izitto/Desktop/Code/PAtDS/twitch_configs.json", "r") as f:
        twitch_configs = json.load(f)
except FileNotFoundError:
    twitch_configs = {}

# Twitch Pages


@app.route('/twitch/home')
def twitch_home():
    return render_template('twitch_manager/twitch_home.html')


@app.route('/twitch/redeems')
def twitch_redeems():
    return render_template('twitch_manager/twitch_redeems.html')
