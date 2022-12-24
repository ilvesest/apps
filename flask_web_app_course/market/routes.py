# local imports
from market import app
from market.models import Item
from market.forms import RegisteredForm

# 3rd party imports
from flask import render_template


# functions
@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register')
def register_page():
    form = RegisteredForm()
    return render_template('register.html', form=form)
    