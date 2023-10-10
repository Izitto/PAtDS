'''from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests
import json
import os
from app import app



# Twitch Pages


@app.route('/twitch/home')
def twitch_home():
    return render_template('twitch_manager/home.html')



@app.route('/twitch/redeems')
def twitch_redeems():
    return render_template('twitch_manager/redeems.html')
'''