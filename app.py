from flask import Flask
from flask import render_template
from datetime import datetime
import re

app = Flask(__name__)

@app.route("/hello/<name>")
def hello(name):
    return render_template(
        "board.html",
        name=name,
        date=datetime.now().strftime("%A, %d %B, %y at %X")
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/get/board")
def home():
    return render_template(
        "board.html"
    )