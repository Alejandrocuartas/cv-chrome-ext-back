""" Flask routes for the app. """

from flask import Flask, request, jsonify
from flask_cors import CORS

from app import utilities

app = Flask(__name__)
CORS(app=app, origins="*")

@app.route('/', methods=['POST'])
def api():
    """ api """
    utilities.extract_data_from_request(request)
    return jsonify({
        'status': 'success'
    })
