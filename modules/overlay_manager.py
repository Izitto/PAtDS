from flask import render_template, flash, jsonify, request
from app import app
import json
# custom overlays


@app.route('/friends', methods=['GET', 'POST'])
def friends():
    return render_template('friends.html')


@app.route('/timers', methods=['GET', 'POST'])
def timers():
    return render_template('timers.html')

# master overlay maker


@app.route('/overlay/sources', methods=['GET', 'POST'])
def overlay():
    return render_template('overlay_manager/overlay_sources.html')


@app.route('/overlay/layout', methods=['GET', 'POST'])
def overlay_layout():
    return render_template('overlay_manager/overlay_layout.html')


@app.route('/overlay/render/<string:overlay_uuid>', methods=['GET', 'POST'])
def render_overlays(overlay_uuid):
    return render_template('overlay_manager/overlay_render.html', overlay_uuid=overlay_uuid)

# overlay api


@app.route('/api/overlay/save_list', methods=['POST'])
def save_list():
    try:
        data = request.json
        with open('/home/izitto/Desktop/Code/PAtDS/list.json', 'w') as f:
            json.dump(data, f)
        return jsonify({"message": "List saved successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "An error occurred while saving the list.", "error": str(e)}), 500


@app.route('/api/overlay/save_sources', methods=['POST'])
def save_sources():
    try:
        data = request.json
        with open('/home/izitto/Desktop/Code/PAtDS/sources.json', 'w') as f:
            json.dump(data, f)
        return jsonify({"message": "Sources saved successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "An error occurred while saving the sources.", "error": str(e)}), 500


@app.route('/api/overlay/get_list', methods=['GET'])
def get_list():
    try:
        with open('/home/izitto/Desktop/Code/PAtDS/list.json', 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": "An error occurred while retrieving the list.", "error": str(e)}), 500


@app.route('/api/overlay/get_sources', methods=['GET'])
def get_sources():
    try:
        with open('/home/izitto/Desktop/Code/PAtDS/sources.json', 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": "An error occurred while retrieving the sources.", "error": str(e)}), 500


