# native imports
from pathlib import Path
import os

# local imports

# 3rd party imports
from flask import Flask
from flask_fontawesome import FontAwesome

# inits
app = Flask(__name__)

# set secret key
app.config['SECRET_KEY'] = 'fwefwefwdf900'
fa = FontAwesome(app)


from dashboard import routes