# local imports
from market import db, bcrypt, login_manager

# 3rd party imports
from flask_login import UserMixin
# callback for the web app. If user is logged in and refreshes or browses through
# the webpage the app keeps them logged in, therefore using different session route 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# UserMixin base class has implemented some callback methods for the user
# to browse in the wwebsite and be kept logged in. 
class User(db.Model, UserMixin):
    
    # 'db.relationship() creates relationla link between Item & User tables
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    # User class attribute 'password'
    @property
    def password(self):
        return self.password

    # 
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # User class method to check input password hash matches hash in db
    def check_password_correction(self, attempted_password) -> bool:
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    @property
    def brittier_budget(self):
        if len(str(self.budget)) >= 3:
            return f'{self.budget:,}'
        else:
            return f"{self.budget}"
        
    def can_purchase(self, item_object):
        return self.budget >= item_object.price
    
    def can_sell(self, item_object):
        return item_object in self.items


# create databse class
class Item(db.Model):
    # 'id' is the convention in Flask apps.
    # limit data length [str] and 30 characters max. No missing values
    # are allowed with 'nullable' and name has to be unique in the table.
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True) 
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    # override the naming convention of the table item
    def __repr__(self):
        return f'Item {self.name}'
    
    def buy(self, user):
        # current_user built-in method accesses logged-in user User object.
        # assigning user id to the Items owner field
        self.owner = user.id
        
        # deduct price of the item from user's budegt
        user.budget -= self.price

        db.session.commit()
        
    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()