from flask import jsonify, request, render_template
from app import app
from modules.VTS.objects import VTS_COORDS, VTS_MODELS, VTS_EXPRESSIONS, VTS_MODEL_POSITIONS, save_VTS_MODEL_POSITIONS, load_VTS_MODEL_POSITIONS
from modules.VTS.send_queue import sender
import modules.VTS.API_requests as API_requests
from modules.shared import emit_socketio_event
import json
# pages

@app.route('/vts/home')
async def vts_home():
    return render_template('vts_manager/home.html')

@app.route('/vts/position_manager')
async def vts_position_manager():
    return render_template('vts_manager/position_manager.html')

# API ENDPOINTS /vts/api/...

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




@app.route('/vts/api/models')
def models():
    models = VTS_MODELS.toJSON()
    return jsonify(success=True, models=models)

@app.route('/vts/api/expressions')
def expressions():
    expressions = VTS_EXPRESSIONS.toJSON()
    return jsonify(success=True, expressions=expressions)

@app.route('/vts/api/coords')
def coords():
    coords = VTS_COORDS.toJSON()
    return jsonify(success=True, coords=coords)

@app.route('/vts/api/modelPositions')
def modelPositions():
    modelPositions = VTS_MODEL_POSITIONS.toJSON()
    return jsonify(success=True, modelPositions=modelPositions)

@app.route('/vts/api/saveModelPositions', methods=['POST'])
def saveModelPositions():
    modelPositions = request.form['modelPositions']
    # modelPositions to python object
    try:
        modelPositionsDict = json.loads(modelPositions)
    except json.JSONDecodeError:
        return jsonify(success=False, message="Invalid JSON format"), 400
    if not isinstance(modelPositionsDict, dict) or "Model_Positions" not in modelPositionsDict:
        return jsonify(success=False, message="Invalid data structure"), 400
    modelPositionsData = modelPositionsDict["Model_Positions"]
    try:
        VTS_MODEL_POSITIONS.addModel_Positions(modelPositionsData)
    except Exception as e:
        # Handle exceptions that could be raised by addModel_Positions
        return jsonify(success=False, message=str(e)), 500
    
    save_VTS_MODEL_POSITIONS()
    return jsonify(success=True)

# api endpoint for setting coords.
# sender(API_requests.setCoords, {"x": 0, "y": 0, "z": 0, "rx": 0, "ry": 0, "rz": 0}) as one dict
# will be recieved as Coords object json
@app.route('/vts/api/setCoords', methods=['POST'])
def setCoords():
    coords = request.form['coords']
    # coords to python object
    try:
        coordsDict = json.loads(coords)
    except json.JSONDecodeError:
        return jsonify(success=False, message="Invalid JSON format"), 400
    if not isinstance(coordsDict, dict) or "Coords" not in coordsDict:
        return jsonify(success=False, message="Invalid data structure"), 400
    coordsData = coordsDict["Coords"]
    try:
        sender(API_requests.moveModel, coordsData)
    except Exception as e:
        # Handle exceptions that could be raised by addCoords
        return jsonify(success=False, message=str(e)), 500
    
    return jsonify(success=True)