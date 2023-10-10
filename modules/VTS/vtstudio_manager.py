from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests
import json
import os
from app import app
import modules.vtstudio as vtstudio
import asyncio

# pages
import asyncio
@app.route('/vts/home')
def vts_home():
    models = vtstudio.VTS_MODELS

    return render_template('vts_manager/home.html', models=models)

@app.route('/vts/api/loadModel', methods=['POST'])
def loadModel():
    print("loadModel() called")
    Model_ID = request.form['Model_ID']
    vtstudio.model_request(Model_ID)
    if vtstudio.VTS_MODELS[Model_ID]['loaded'] == True:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/vts/api/setExpression', methods=['POST'])
def setExpression():
    print("setExpression() called")
    file = request.form['file']
    active = request.form['active']
    vtstudio.expression_request(file, active)
    return jsonify({'success': True})


# API ENDPOINTS /vts/api/...

