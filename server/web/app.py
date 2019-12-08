from flask import Flask, jsonify
from flask_cors import CORS
from modules.extract import extract_data
import os

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/freqdist', methods=['GET'])
def getfreqDist():
    data = extract_data()
    return jsonify(data)


@app.route("/")
def entry():
    data_dir = "../data"
    print(os.getcwd())
    return jsonify(os.listdir(data_dir))
