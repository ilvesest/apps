from market import db

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
    
    # override the naming convention of the table item
    def __repr__(self):
        return f'Item {self.name}'