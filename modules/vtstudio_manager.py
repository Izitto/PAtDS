from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests
import json
import os
from app import app
import modules.vtstudio as vtstudio

# pages
@app.route('/vts/home')
def twitch_home():
    return render_template('vts_manager/home.html')

# API ENDPOINTS

@app.route('/vts/api/load_model', methods=['POST'])
def load_model():
    model_id = request.json.get('model_id')
    vtstudio.VTubeStudioAPI.load_model(model_id)
    return jsonify({'success': True})

@app.route('/vts/api/get_current_loaded_model_id', methods=['GET'])
def get_current_loaded_model_id():
    current_model_id = vtstudio.VTubeStudioAPI.get_current_loaded_model_id()
    return jsonify({'current_model_id': current_model_id})

@app.route('/vts/api/get_hotkey_list', methods=['GET'])
def get_hotkey_list():
    hotkey_list = vtstudio.VTubeStudioAPI.get_hotkey_list()
    return jsonify({'hotkey_list': hotkey_list})

@app.route('/vts/api/trigger_hotkey', methods=['POST'])
def trigger_hotkey():
    hotkey_id = request.json.get('hotkey_id')
    vtstudio.VTubeStudioAPI.trigger_hotkey(hotkey_id)
    return jsonify({'success': True})

@app.route('/vts/api/get_expression_list', methods=['GET'])
def get_expression_list():
    expression_list = vtstudio.VTubeStudioAPI.get_expression_list()
    return jsonify({'expression_list': expression_list})

@app.route('/vts/api/get_current_expression', methods=['GET'])
def get_current_expression():
    current_expression = vtstudio.VTubeStudioAPI.get_current_expression()
    return jsonify({'current_expression': current_expression})

@app.route('/vts/api/set_expression', methods=['POST'])
def set_expression():
    expression_id = request.json.get('expression_id')
    vtstudio.VTubeStudioAPI.set_expression(expression_id)
    return jsonify({'success': True})


@app.route('/vts/api/get_all_model_icons', methods=['GET'])
def get_all_model_icons():
    model_icons = vtstudio.VTubeStudioAPI.get_all_model_icons()
    return jsonify({'model_icons': model_icons})

@app.route('/vts/api/get_current_model_icon', methods=['GET'])
def get_current_model_icon():
    current_model_icon = vtstudio.VTubeStudioAPI.get_current_model_icon()
    return jsonify({'current_model_icon': current_model_icon})
