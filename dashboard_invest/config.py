# native imports
import os

class Config(object):
    DEBUG = True,
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fwefwefwdf900',
    
    # Flask-Caching configs
    CACHE_TYPE = "SimpleCache",
    CACHE_DEFAULT_TIMEOUT = 200
    
    