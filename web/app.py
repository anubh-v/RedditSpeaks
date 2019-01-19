from flask import Flask
from modules.extract import extract_data

app = Flask(__name__)

@app.route("/")
def entry():
    return extract_data()

