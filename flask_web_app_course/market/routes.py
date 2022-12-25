# local imports
from market import app, db
from market.models import Item, User
from market.forms import RegisteredForm

# 3rd party imports
from flask import render_template, redirect, url_for


# functions
@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisteredForm()
    
    # submit button validation and add created data to database
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password_hash=form.password1.data)
        # send data to database
        db.session.add(user_to_create)
        db.session.commit()
        
        # redirect person to new page
        return redirect(url_for('market_page'))
    
    # if errors occur they are sent to forms.errors
    if form.errors != {}: # if tehre are errors
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')
    
    
    return render_template('register.html', form=form)
    