from config import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class Educator(db.Model):
    # define the table name for the database
    __tablename__ = "educators"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String, nullable=False)
    d_o_b = db.Column(db.Date, default="")
    phone_number = db.Column(db.String(), nullable=False, unique=True)
    
    # Define a relationship with the "Course" model, linking "educator" and "courses"
    courses = db.relationship("Course", back_populates="educator", cascade="all, delete")

# Create the EducatorSchema with marshmallow 
class EducatorSchema(ma.Schema):
    #Validation
    email = fields.Email()
    password = fields.String(validate=(
        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[A-Za-z0-9]{8,}$", 
            error="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")))
    d_o_b = fields.Date(format="%Y-%m-%d")
    phone_number = fields.String(validate=(
        Regexp("^[0-9]{10}$", error="Phone number should contain exactly 10 numbers.")))
    
    # Nested field for multiple courses
    courses = fields.Nested("CourseSchema", many=True, only= ("id", "title"))
    class Meta:
        ordered = True
        fields = ("id", "email", "password", "name", "d_o_b", "phone_number", "", "courses")
