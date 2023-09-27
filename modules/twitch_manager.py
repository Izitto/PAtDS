from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests
import json
import os
from app import app
from twitchio.ext import commands


# Load Twitch Configurations
twitch_configs = {}
config_missing = False  # New variable to track missing configs
twitch_bot = None
try:
    with open("/home/izitto/Documents/Code/PAtDS/twitch_configs.json", "r") as f:
        content = f.read().strip()
        if content:
            twitch_configs = json.loads(content)
except json.JSONDecodeError:
    print("JSON Decode Error: The file is not a valid JSON. Using default settings.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Check if required configs are missing
if not twitch_configs.get('client_id') or not twitch_configs.get('irc_token'):
    config_missing = True  # Update the variable if configs are missing


# Function to initialize Twitch Bot
def initialize_twitch_bot():
    global twitch_bot
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
    if config_missing:
        flash('Twitch configurations are missing. Please enter them.', 'warning')
    # Your code to get Twitch stream title, category, and live status
    title = "Your Stream Title"
    category = "Your Stream Category"
    live_status = "Live or Offline"
    return render_template('twitch_manager/home.html', title=title, category=category, live_status=live_status)



@app.route('/twitch/redeems')
def twitch_redeems():
    return render_template('twitch_manager/redeems.html')


@app.route('/twitch/save_twitch_configs', methods=['POST'])
def save_twitch_configs():
    global twitch_configs, config_missing  # Declare them as global to modify
    client_id = request.form.get('client_id')
    irc_token = request.form.get('irc_token')
    
    twitch_configs['client_id'] = client_id
    twitch_configs['irc_token'] = irc_token
    
    # Save to file
    try:
        with open("/home/izitto/Documents/Code/PAtDS/twitch_configs.json", "w") as f:
            json.dump(twitch_configs, f)
        config_missing = False  # Update the flag
        initialize_twitch_bot()  # Initialize the Twitch Bot here
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/twitch/get_twitch_info', methods=['GET'])
def get_twitch_info():
    # Your code to get Twitch stream title, category, and live status
    title = "Your Updated Stream Title"
    category = "Your Updated Stream Category"
    live_status = "Live or Offline"
    
    return jsonify({'title': title, 'category': category, 'live_status': live_status})



@app.route('/authorize_twitchio')
def authorize_twitchio():
    # Your code to authorize Twitchio goes here
    return redirect(url_for('twitch_home'))
