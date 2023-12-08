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

    # Define a relationship with the "Enrolment" model, linking "user" and "enrolments"
    enrolments = db.relationship("Enrolment", back_populates="user", cascade="all, delete")

    # Define a relationship with the "Review" model, linking "user" and "reviews"
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete")




# Create the UserSchema with marshmallow 
class UserSchema(ma.Schema):
    # Nested field for multiple enrolments
    enrolments = fields.Nested("EnrolmentSchema", many=True, only=["course"])
    # Nested field for multiple reviews
    reviews = fields.Nested("ReviewSchema", many=True, exclude=["user"])

    class Meta:
        ordered = True
        fields = ("id", "email", "password", "name", "d_o_b", "phone_number", "enrolments", "reviews")