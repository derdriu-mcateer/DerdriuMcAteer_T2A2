from config import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class User(db.Model):
    # define the table name for the database
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String, nullable=False)
    d_o_b = db.Column(db.Date, default="N/A")
    phone_number = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    

    # Define a relationship with the "Enrolment" model, linking "user" and "enrolments"
    enrolments = db.relationship("Enrolment", back_populates="user", cascade="all, delete")

    # Define a relationship with the "Review" model, linking "user" and "reviews"
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete")




# Create the UserSchema with marshmallow 
class UserSchema(ma.Schema):
    #Validation
    email = fields.Email()
    password = fields.String(validate=(
        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[A-Za-z0-9]{8,}$", 
            error="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")))
    d_o_b = fields.Date(format="%Y-%m-%d")
    phone_number = fields.String(validate=(
        Regexp("^[0-9]{10}$", error="Phone number should contain exactly 10 numbers.")))
    
    # Nested field for multiple enrolments
    enrolments = fields.Nested("EnrolmentSchema", many=True, only=["course"])
    # Nested field for multiple reviews
    reviews = fields.Nested("ReviewSchema", many=True, exclude=["user"])

    class Meta:
        ordered = True
        fields = ("id", "email", "password", "name", "d_o_b", "phone_number", "is_admin", "enrolments", "reviews")

