from flask import Flask
from flask import render_template
from modules.extract import extract_data

app = Flask(__name__)


@app.route("/")
def entry():
    data = extract_data()
    return render_template("index.html", data=data)
    # return extract_data()
