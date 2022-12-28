# local module imports
from market.models import User

# 3rd party imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class RegisteredForm(FlaskForm):
    
    # FlaskForm will validate the username via 'validate_' 'username' function name.
    # flask validates if it sees prefix 'validate_' in function name and looks for 
    # field 'username' in the User database.
    def validate_username(self, username_to_check: str):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')
    
    def validate_email(self, email_to_check: str):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email address already exists! Please try a different email address.')
        
    
    username = StringField(
        label='User Name:', 
        validators=[Length(min=2, max=30), DataRequired()])
    
    email = StringField(
        label='Email Address:',
        validators=[Email(), DataRequired()])
    
    password1 = PasswordField(
        label='Password:',
        validators=[Length(min=6), DataRequired()])
    
    password2 = PasswordField(
        label='Confirm Password:',
        validators=[EqualTo('password1'), DataRequired()])
    
    submit = SubmitField(label='Create Account')
    
class LoginForm(FlaskForm):
    
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')
    

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Confirm')
    
class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')