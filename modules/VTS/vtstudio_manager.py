from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests
import json
import os
from app import app
import modules.VTS.vtstudio as vtstudio
from modules.VTS.send_queue import sender
import modules.VTS.API_requests as API_requests
import asyncio
from modules.shared import emit_socketio_event
# pages
import asyncio
@app.route('/vts/home')
async def vts_home():
    models = API_requests.VTS_MODELS.getModels()
    expressions = vtstudio.VTS_EXPRESSIONS.getExpressions()

    return render_template('vts_manager/home.html', models=models, expressions=expressions)

@app.route('/vts/api/loadModel', methods=['POST'])
async def loadModel():
    Model_ID = request.form['Model_ID']
    await sender(API_requests.loadModel, Model_ID)
    emit_socketio_event("vts_api", "model request: " + Model_ID)
    # API_requests.send.put_nowait(Model_ID)

    return jsonify({'success': True})

@app.route('/vts/api/setExpression', methods=['POST'])
async def setExpression():
    file = request.form['file']
    active = request.form['active']
    emit_socketio_event("vts_api", "expression request: " + file + " " + active)
    await sender(API_requests.setExpression, {"file": file, "status": active})
    return jsonify({'success': True})


# API ENDPOINTS /vts/api/...

@app.route('/vts/api/models')
def models():
    models = API_requests.VTS_MODELS.toJSON()
    return jsonify(success=True, models=models)

@app.route('/vts/api/expressions')
def expressions():
    expressions = vtstudio.VTS_EXPRESSIONS.toJSON()
    return jsonify(success=True, expressions=expressions)