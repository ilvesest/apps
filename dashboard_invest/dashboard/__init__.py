# native imports

# local imports
from config import Config

# 3rd party imports
from flask import Flask
from flask_caching import Cache
from flask_fontawesome import FontAwesome


config = {
    "DEBUG": True,                # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

# inits
app = Flask(__name__)

# set some environment variables from the config file
app.config.from_object(Config)

# flask-caching isntance
#cache = Cache(app)
 
#fa = FontAwesome(app)

# Flask convention to bypass circular imports by placing routes import in the bottom 
from dashboard import routes