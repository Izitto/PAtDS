from flask import render_template, flash, jsonify, request
from app import app
import json, uuid, os
from modules.shared import report_error
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

# object to load

class Overlay:
    def __init__(self):
        self.UUID: str
        self.name: str
        self.script: str
        self.style: str
        self.sourceUUID: []

class Source:
    def __init__(self):
        self.UUID: str
        self.name: str
        self.url: str
        self.height: float
        self.width: float
        self.x: float
        self.y: float

Overlays = Overlay()
Sources = Source()


# load and save objects from and to json files
# need a function to load and save overlays and sources as a list of objects to json files

def load_overlays():
    global Overlays
    try:
        with open('/home/izitto/Desktop/Code/PAtDS/variables/overlays.json', 'r') as f:
            data = json.load(f)
            Overlays = [Overlay(overlay["UUID"], overlay["id"], overlay["name"], overlay["script"], overlay["style"], overlay["sourceUUID"]) for overlay in data["Overlays"]]
    except Exception as e:
        report_error(e)

def load_sources():
    global Sources
    try:
        with open('/home/izitto/Desktop/Code/PAtDS/variables/sources.json', 'r') as f:
            data = json.load(f)
            Sources = [Source(source["UUID"], source["name"], source["url"], source["height"], source["width"], source["x"], source["y"]) for source in data["Sources"]]
    except Exception as e:
        report_error(e)

def save_overlays(overlay):
    # check if overlay is different from the one in the list
    global Overlays
    if overlay not in Overlays:
        # if it is, update the list
        Overlays.append(overlay)
        # save the list to json file
        try:
            with open('/home/izitto/Desktop/Code/PAtDS/variables/overlays.json', 'w') as f:
                json.dump(Overlays, f)
        except Exception as e:
            report_error(e)
        
def save_sources(source):
    # check if source is different from the one in the list
    global Sources
    if source not in Sources:
        # if it is, update the list
        Sources.append(source)
        # save the list to json file
        try:
            with open('/home/izitto/Desktop/Code/PAtDS/variables/sources.json', 'w') as f:
                json.dump(Sources, f)
        except Exception as e:
            report_error(e)



# new endpoints with better data structure

@app.route('/api/v2/save_overlays', methods=['POST'])
def save_overlays_route():
    save_overlays(request.json)
    return jsonify({"message": "Overlays saved successfully!"}), 200



@app.route('/api/v2/load_overlays', methods=['GET'])
def load_overlays_route():
    return jsonify(Overlays), 200

@app.route('/api/v2/save_sources', methods=['POST'])
def save_sources_route():
    save_sources(request.json)
    return jsonify({"message": "Sources saved successfully!"}), 200

@app.route('/api/v2/load_sources', methods=['GET'])
def load_sources_route():
    return jsonify(Sources), 200