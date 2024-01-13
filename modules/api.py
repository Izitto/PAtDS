import modules.Control as control
from flask import render_template, request, jsonify, send_from_directory, abort
from app import app
import pymysql
import requests
import modules.shared as shared
neko_timer = shared.neko_timer
derp_timer = shared.derp_timer
host = shared.host
user = shared.user
password = shared.password
database = shared.database
viewer = shared.viewer
friend = shared.friend
import os
# import modules.module_control as module_control
# route for audio files
@app.route('/api/audio/<filename>', methods=['GET'])
def get_audio(filename):
    print("Called: /api/audio/" + filename)
    try:
        return send_from_directory(app.static_folder + '/audio', filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/api/images/<filename>', methods=['GET'])
def get_image(filename):
    print("Called: /api/images/" + filename)
    try:
        return send_from_directory(app.static_folder + '/images', filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/api/images/<foldername>/<filename>', methods=['GET'])
def get_folder_image(foldername, filename):
    print("Called: /api/images/" + foldername + "/" + filename)
    full_path = app.static_folder + '/images/' + foldername + "/"
    try:
        return send_from_directory(full_path, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/api/store_image/<filename>', methods=['POST'])
def store_image(foldername, filename):
    print("Called: /api/store_image/" + foldername + "/" + filename)
    image = request.files['image']
    full_path = app.static_folder + '/images/' + foldername + "/"
    image.save(full_path + filename)
    return "image saved"

@app.route('/api/tn/temp_bg', methods=['POST'])
def save_temp_bg():
    # Get the URL from the request data
    image_url = request.json.get('url')
    
    # Fetch the image from the provided URL
    response = requests.get(image_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Define the path to save the image
        save_path = app.static_folder+ '/images/tn/temp_bg.png'
        # Save the image
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        # Return the saved image
        directory_path = os.path.join(app.static_folder, 'images', 'tn')
        return send_from_directory(directory_path, 'temp_bg.png', as_attachment=True)
    else:
        return jsonify({"error": "Failed to fetch the image"}), 500



@app.route('/api/commands', methods=['POST'])
def commands():
    print("Called: /api/commands")
    term = request.json.get('term')
    control.commands(term)
    return jsonify(screen=control.screen, ccard=control.ccard)



@app.route('/api/get_HDMI', methods=['GET'])
def get_HDMI():
    print("Called: /api/get_HDMI")
    return jsonify(screen=control.screen, ccard=control.ccard)


@app.route('/api/notify_neko', methods=['POST'])
def notify_neko():
    print("Called: /api/notify_neko")
    up = request.json.get('up')
    shared.emit_socketio_event('wake_up', 'hello')
    shared.emit_socketio_event('neko_state', {'up': up, })
    return "timer set"


@app.route('/api/notify_derp', methods=['POST'])
def notify_derp():
    print("Called: /api/notify_derp")
    up = request.json.get('up')
    shared.emit_socketio_event('wake_up', 'hello')
    shared.emit_socketio_event('derp_state', {'up': up, })
    return "notification sent"


@app.route('/api/set_neko_timer', methods=['POST'])
def set_timer():
    print("Called: /api/set_neko_timer")
    global neko_timer
    neko_timer = request.json.get('timer')
    shared.emit_socketio_event('neko_timer_updated', {
                               'message': 'Neko timer updated'})
    return "timer set"


@app.route('/api/set_derp_timer', methods=['POST'])
def set_derp_timer():
    print("Called: /api/set_derp_timer")
    global derp_timer
    derp_timer = request.json.get('timer')
    shared.emit_socketio_event('derp_timer_updated', {
                               'message': 'Derp timer updated'})
    return "timer set"


@app.route('/api/get_neko_timer', methods=['GET'])
def get_timer():
    print("Called: /api/get_neko_timer")
    global neko_timer
    return jsonify(timer=neko_timer)


@app.route('/api/get_derp_timer', methods=['GET'])
def get_derp_timer():
    print("Called: /api/get_derp_timer")
    global derp_timer
    return jsonify(timer=derp_timer)


@app.route('/api/friend')
def send_friend():
    print("Called: /api/friend")
    db = pymysql.connect(host=host, user=user,
                         password=password, database=database)
    cursor = db.cursor()
    sql = "SELECT name FROM friend_viewer_names WHERE type='friend'"
    cursor.execute(sql)
    friend_results = cursor.fetchall()
    friend_name = [result[0] for result in friend_results]
    sql = "UPDATE friend_viewer_names SET name=NULL WHERE type='friend'"
    cursor.execute(sql)
    db.commit()
    db.close()
    return jsonify(friend=friend_name)


@app.route('/api/viewer')
def send_viewer():
    print("Called: /api/viewer")
    db = pymysql.connect(host=host, user=user,
                         password=password, database=database)
    cursor = db.cursor()
    sql = "SELECT name FROM friend_viewer_names WHERE type='viewer'"
    cursor.execute(sql)
    viewer_results = cursor.fetchall()
    viewer_name = [result[0] for result in viewer_results]
    sql = "UPDATE friend_viewer_names SET name=NULL WHERE type='viewer'"
    cursor.execute(sql)
    db.commit()
    db.close()
    return jsonify(viewer=viewer_name)

# get the friend names from client and store them in the database


@app.route('/api/get_friend', methods=['POST'])
def get_friend():
    print("Called: /api/get_friend")
    db = pymysql.connect(host=host, user=user,
                         password=password, database=database)
    cursor = db.cursor()
    sql = "UPDATE friend_viewer_names SET name=%s WHERE type='friend'"
    cursor.execute(sql, (request.form['friend'],))
    db.commit()
    db.close()
    shared.emit_socketio_event(
        'friend_updated', {'message': 'Friend list updated'})
    return "friend name received"

# get the viewer name from client and store it in the database


@app.route('/api/get_viewer', methods=['POST'])
def get_viewer():
    print("Called: /api/get_viewer")
    db = pymysql.connect(host=host, user=user,
                         password=password, database=database)
    cursor = db.cursor()
    sql = "UPDATE friend_viewer_names SET name=%s WHERE type='viewer'"
    cursor.execute(sql, (request.form['viewer'],))
    db.commit()
    db.close()
    shared.emit_socketio_event(
        'viewer_updated', {'message': 'Viewer list updated'})
    return "viewer name received"


def set_names_to_null():
    db = pymysql.connect(host=host, user=user,
                         password=password, database=database)
    cursor = db.cursor()
    sql = "UPDATE friend_viewer_names SET name=NULL WHERE type='friend' OR type='viewer'"
    cursor.execute(sql)
    db.commit()
    db.close()

# keep alive
@app.route('/api/keep_alive', methods=['GET'])
def keep_alive():
    print("Called: /api/keep_alive")
    page = request.args.get('page')
    print("page: ", page)
    return jsonify({'status': 'success', 'message': 'Connection kept alive'}), 200

#route for getting user configs
@app.route('/api/get_user_configs', methods=['GET'])
def get_user_configs():
    print("Called: /api/get_user_configs")
    # user defines the object and value to return
    group = request.args.get('group')
    object = request.args.get('object')
    value = request.args.get('value')
    user_configs = shared.fetch_user_configs()
    # return the object and value
    if group:
        return jsonify(user_configs[group][object][value]), 200
    else:
        return jsonify(user_configs[object][value]), 200



@app.route('/api/friend_list')
def get_friend_list():
    with open('/home/izitto/Desktop/Code/PAtDS/static/friends.txt', 'r') as f:
        friend_list = [line.strip() for line in f.readlines()]
    return jsonify(friend_list)

'''
@app.route('/api/modules/start', methods=['POST'])
def start_modules():
    module_control.start()
    return "module started"

@app.route('/api/modules/kill', methods=['POST'])
def kill_modules():
    module_control.kill()
    return "module killed"

@app.route('/api/modules/status', methods=['POST'])
def module_status():
    return jsonify(module_control.status())
'''

