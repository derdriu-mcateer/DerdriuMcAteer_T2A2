from setup import db, ma
from marshmallow import fields
class User(db.Model):
    # define the table name for the database
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String, nullable=False)
    d_o_b = db.Column(db.Date, default="")
    phone_number = db.Column(db.String(), nullable=False, unique=True)

    enrolments = db.relationship('Enrolment', back_populates='user', cascade='all, delete')

    reviews = db.relationship('Review', back_populates='user', cascade='all, delete')




# Create the UserSchema with marshmallow 
class UserSchema(ma.Schema):
    reviews = fields.Nested('ReviewSchema', many=True, exclude=['user'])
    enrolments = fields.Nested('EnrolmentSchema', many=True, only=['course'])
    class Meta:
        ordered = True
        fields = ("id", "email", "password", "name", "d_o_b", "phone_number", "enrolments", 'reviews')