# native imports
from pathlib import Path

# 3rd party imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# inits
app = Flask(__name__) # __name__ refs to the current local py file

# point to the absolute path of the .db file (in Unix systems)
root_abs_path = Path.cwd()
project_db_path = '/market/market.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{root_abs_path}{project_db_path}'
app.config['SECRET_KEY'] = '40217598b125400a38f5a01f'

# store passwords as hashes not plain text
bcrypt = Bcrypt(app)

# init database
db = SQLAlchemy(app) # database

# use it here to bypass circular import error
from market import routes