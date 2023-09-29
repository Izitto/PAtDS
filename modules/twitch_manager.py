from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests
import json
import os
from app import app
from twitchio.ext import commands


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
