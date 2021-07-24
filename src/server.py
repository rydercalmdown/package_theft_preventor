"""Components for running the raspberry pi in server mode"""

import os
from flask import Flask, jsonify
from relay_controller import RelayController


app = Flask(__name__)
rc = RelayController()


@app.route('/')
def index():
    """API index route"""
    return jsonify({'status': 'ok'})


@app.route('/alarm/')
def alarm():
    """Turn on the relay"""
    rc.activate_general_alarm()
    return jsonify({'status': 'alarm activated'})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
