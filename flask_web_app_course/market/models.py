from market import db

class User(db.Model):
    # 'db.relationship() creates relationla link between Item & User tables
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

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