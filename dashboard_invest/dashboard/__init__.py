# native imports
from pathlib import Path

# local imports

# 3rd party imports
from flask import Flask
from flask_fontawesome import FontAwesome

# inits

app = Flask(__name__)

fa = FontAwesome(app)

from dashboard import routes