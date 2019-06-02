from flask import Flask, jsonify, request
from flask import render_template
from flask_cors import CORS
from modules.extract import extract_data

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route("/")
def entry():
    data = extract_data()
    return render_template("index.html", data=data)
    # return extract_data()
