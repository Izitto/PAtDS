from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests
import json
import os
from app import app
import modules.vtstudio as vtstudio


@app.route('/vts/home')
def twitch_home():
    return render_template('twitch_manager/home.html')

@app.route('/vts/change_model', methods=['POST'])
def twitch_change_model():
    model_id = request.form['model_id']
    vtstudio.VTubeStudioAPI().load_model(model_id)
    return redirect(url_for('twitch_home'))

@app.route('/vts/change_expression', methods=['POST'])
def twitch_change_expression():
    expression_id = request.form['expression_id']
    vtstudio.VTubeStudioAPI().trigger_hotkey(expression_id)
    return redirect(url_for('twitch_home'))

@app.route('/vts/trigger_hotkey', methods=['POST'])
def twitch_change_hotkey():
    hotkey_id = request.form['hotkey_id']
    vtstudio.VTubeStudioAPI().trigger_hotkey(hotkey_id)
    return redirect(url_for('twitch_home'))

@app.route('/vts/get_model_id', methods=['GET'])
def twitch_get_model_id():
    return jsonify(vtstudio.VTubeStudioAPI().get_current_loaded_model_id())

@app.route('/vts/get_hotkey_list', methods=['GET'])
def twitch_get_hotkey_list():
    return jsonify(vtstudio.VTubeStudioAPI().get_hotkey_list())

@app.route('/vts/get_expression_list', methods=['GET'])
def twitch_get_expression_list():
    return jsonify(vtstudio.VTubeStudioAPI().get_expression_list())

@app.route('/vts/get_model_list', methods=['GET'])
def twitch_get_model_list():
    return jsonify(vtstudio.VTubeStudioAPI().get_model_list())

@app.route('/vts/get_model_info', methods=['GET'])
def twitch_get_model_info():
    model_id = request.args.get('model_id')
    return jsonify(vtstudio.VTubeStudioAPI().get_model_info(model_id))

@app.route('/vts/get_model_thumbnail', methods=['GET'])
def twitch_get_model_thumbnail():
    model_id = request.args.get('model_id')
    return jsonify(vtstudio.VTubeStudioAPI().get_model_thumbnail(model_id))

