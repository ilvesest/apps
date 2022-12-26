# local imports
from market import app, db
from market.models import Item, User
from market.forms import RegisteredForm, LoginForm

# 3rd party imports
from flask import render_template, redirect, url_for, flash
from flask_login import login_user


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
    
    # when submit is pressed it validates if no errors occured
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
    if form.validate_on_submit():
        # if user excists. first() is used to get the object from query
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            # when entered username and password are correct log in
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            
            return redirect(url_for('market_page'))
        
        else:
            flash('Username and password do not match! Please try again!', category='danger')
        
    return render_template('login.html', form=form)

