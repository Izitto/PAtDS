import modules.Control as Control
from app import app
# ###################################################
# if you don't understand, smoke crack first and try again
if __name__ == '__main__':
    Control.start()
    app.run(debug=True, port=5000, host='0.0.0.0')
    Control.join()