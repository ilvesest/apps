# native imports

# local imports

# 3rd party imports
from flask import Flask
from config import Config
from flask_fontawesome import FontAwesome

# inits
app = Flask(__name__)

# set some environment variables from the config file
app.config.from_object(Config)

fa = FontAwesome(app)

# Flask convention to bypass circular imports by placing routes import in the bottom 
from dashboard import routes