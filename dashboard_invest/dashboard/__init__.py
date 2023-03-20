# native imports
import os

# local imports
from config import Config

# 3rd party imports
from flask import Flask
from flask_caching import Cache
from flask_fontawesome import FontAwesome


config = {
    # Flask configs
    "DEBUG": True,                
    'SECRET_KEY': os.environ.get('SECRET_KEY') or 'fwefwefwdf900',
    
    # Flask-Caching configs
    "CACHE_TYPE": "SimpleCache",  
    "CACHE_DEFAULT_TIMEOUT": 300  
}

# inits
app = Flask(__name__)

# set some environment variables from the config file
#app.config.from_object(Config)
app.config.from_mapping(config)

# flask-caching isntance
cache = Cache(app)
 
#fa = FontAwesome(app)

# Flask convention to bypass circular imports by placing routes import in the bottom 
from dashboard import routes