from setup import db, ma

class User(db.Model):
    # define the table name for the database
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String, nullable=False)
    d_o_b = db.Column(db.Date, default="")
    phone_number = db.Column(db.String(), nullable=False, unique=True)

# Create the UserSchema with marshmallow 
class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "email", "password", "name", "d_o_b", "phone_number")