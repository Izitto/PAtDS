from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests
import json
import os
from app import app
import modules.vtstudio as vtstudio
import asyncio

# pages
import asyncio
vtstudio.search_api_server()
@app.route('/vts/home')
def vts_home():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    models = loop.run_until_complete(vtstudio.get_available_models())
    return render_template('vts_manager/home.html', models=models)




# API ENDPOINTS /vts/api/...

