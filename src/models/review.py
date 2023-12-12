from config import db, ma
from marshmallow import fields

# Course class inherits from db.Model allowing it to map objects to corresponding db tables
class Review(db.Model):
    # define the table name for the database
    __tablename__= "reviews"
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False)
 
    # Define a column for storing the foreign key referencing the "id" column in the "users" table
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Define a relationship with the "User" model, linking "reviews" and "user"
    user = db.relationship("User", back_populates="reviews")

    # Define a column for storing the foreign key referencing the "id" column in the "courses" table
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"),nullable=False)
     # Define a relationship with the "Educator" model, linking "reviews" and "course"
    course = db.relationship("Course", back_populates="reviews")
    

# Create the CourseSchema with marshmallow 
class ReviewSchema(ma.Schema):
    user_id = fields.Integer()
    course_id = fields.Integer()
    description = fields.String(required=True)
    user = fields.Nested("UserSchema", only=["id", "name"])
    course = fields.Nested("CourseSchema", only=["id", "title"])

    description = fields.String(required=True)  # Assuming description is a required field

    class Meta:
        fields = ("id", "description", "user", "course")