# System imports
import json
# Flask imports
from flask import Flask

app = Flask(__name__)
app.config.from_file('config.json', load=json.load)
