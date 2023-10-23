from flask import jsonify, request, render_template
from app import app
import modules.VTS.vtstudio as vtstudio
from modules.VTS.objects import VTS_COORDS, VTS_MODELS, VTS_EXPRESSIONS
from modules.VTS.send_queue import sender
import modules.VTS.API_requests as API_requests
from modules.shared import emit_socketio_event

# pages

@app.route('/vts/home')
async def vts_home():
    return render_template('vts_manager/home.html')

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