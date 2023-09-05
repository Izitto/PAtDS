from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests
import json
import os
from app import app
from twitchio.ext import commands


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

# Initialize Twitch Bot
twitch_bot = commands.Bot(
    irc_token=twitch_configs.get('irc_token', ''),
    client_id=twitch_configs.get('client_id', ''),
    nick=twitch_configs.get('nick', ''),
    prefix=twitch_configs.get('prefix', '!'),
    initial_channels=[twitch_configs.get('channel', '')]
)



async def update_twitch_info(title, category):
    headers = {
        'Client-ID': twitch_configs.get('client_id', ''),
        'Authorization': f"Bearer {twitch_configs.get('oauth_token', '')}"
    }
    data = {
        'title': title,
        'game_id': category  # You may need to convert category to game_id
    }
    response = requests.patch('https://api.twitch.tv/helix/channels', headers=headers, json=data)
    return response.json()



# Twitch Pages


@app.route('/twitch/home')
def twitch_home():
    # Your code to get Twitch stream title, category, and live status
    title = "Your Stream Title"
    category = "Your Stream Category"
    live_status = "Live or Offline"
    return render_template('twitch_manager/home.html', title=title, category=category, live_status=live_status)



@app.route('/twitch/redeems')
def twitch_redeems():
    return render_template('twitch_manager/redeems.html')
