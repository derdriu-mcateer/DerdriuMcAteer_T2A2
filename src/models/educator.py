from setup import db, ma
from marshmallow import fields

class Educator(db.Model):
    # define the table name for the database
    __tablename__ = "educators"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String, nullable=False)
    d_o_b = db.Column(db.Date, default="")
    phone_number = db.Column(db.String(), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean(), default=False)
    courses = db.relationship("Course", back_populates="educator", cascade="all, delete")

# Create the EducatorSchema with marshmallow 
class EducatorSchema(ma.Schema):
    courses = fields.Nested("CourseSchema", many=True, only= ("id", "title"))
    class Meta:
        ordered = True
        fields = ("id", "email", "password", "name", "d_o_b", "phone_number", "is_admin", "courses")
