# native imports
from pathlib import Path

# 3rd party imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# inits
app = Flask(__name__) # __name__ refs to the current local py file

# point to the absolute path of the .db file (in Unix systems)
root_abs_path = Path.cwd()
project_db_path = '/market/market.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{root_abs_path}{project_db_path}'

db = SQLAlchemy(app) # database

from market import routes