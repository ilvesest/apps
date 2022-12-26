# local imports
from market import app, db
from market.models import Item, User
from market.forms import RegisteredForm, LoginForm

# 3rd party imports
from flask import render_template, redirect, url_for, flash


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
                              password=form.password1.data)
        # send data to database
        db.session.add(user_to_create)
        db.session.commit()
        
        # redirect person to new page
        return redirect(url_for('market_page'))
    
    # if errors occur they are sent to forms.errors
    if form.errors != {}: # if tehre are errors
        for err_msg in form.errors.values():
            # 
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)
    