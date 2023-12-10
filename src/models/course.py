from setup import db, ma
from datetime import datetime
from marshmallow import fields

# Course class inherits from db.Model allowing it to map objects to corresponding db tables
class Course(db.Model):
    # Define the table name for the database
    __tablename__= "courses"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    date = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))
    description = db.Column(db.String(), nullable=False)
    duration = db.Column(db.String(), nullable=False)

    # Define a column for storing the foreign key referencing the "id" column in the "educators" table
    educator_id = db.Column(db.Integer, db.ForeignKey("educators.id"),nullable=False)
    # Define a relationship with the "Educator" model, linking "courses" and "educators"
    educator = db.relationship("Educator", back_populates="courses")

    # Define a relationship with the "Enrolment" model, linking "course" and "enrolments"
    enrolments = db.relationship("Enrolment", back_populates="course", cascade="all, delete")

    # Define a relationship with the "Review" model, linking "course" and "reviews"
    reviews = db.relationship("Review", back_populates="course", cascade="all, delete")

# Create the CourseSchema with marshmallow 
class CourseSchema(ma.Schema):
    #Validation 
    title = fields.String(required=True)
    date = fields.Date(format="%Y-%m-%d")
    description = fields.String(required=True)
    duration =fields.String(required=True)

    educator_id = fields.Integer()
    educator = fields.Nested("EducatorSchema", only=("name", "email"))
    # Nested field for multiple users
    enrolments = fields.Nested("EnrolmentSchema", many=True, only=["user"])
    # Nested field for multiple reviews
    reviews = fields.Nested("ReviewSchema", many=True,exclude=["course"])


    class Meta:
        ordered = True
        fields = ("id", "title","date", "description", "duration","educator_id", "educator", "enrolments", "reviews")