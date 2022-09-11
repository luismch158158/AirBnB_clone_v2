#!/usr/bin/python3
"""Script to starts a Flask web application"""
from flask import Flask
from markupsafe import escape
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_world():
    """Return message"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hello_HBNB():
    """Return message HBNB"""
    return "HBNB"


@app.route("/c/<string:text>", strict_slashes=False)
def variable_text(text):
    """Return text variable"""
    new_text = text.replace('_', ' ')
    return ('C {:s}'.format(escape(new_text)))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
