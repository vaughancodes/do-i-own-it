# Python built-in
import os
import json
import urllib
import logging

# External packages
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")

db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run()
