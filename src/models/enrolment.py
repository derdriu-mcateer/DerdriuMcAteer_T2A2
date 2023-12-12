from config import db, ma
from marshmallow import fields


class Enrolment(db.Model):
    # Define the table name for the database
    __tablename__ = 'enrolments'

    id = db.Column(db.Integer, primary_key=True)

    # Define a column for storing the foreign key referencing the "id" column in the "users" table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Define a relationship with the "User" model, linking "users" and "enrolments"
    user = db.relationship('User', back_populates='enrolments')

    # Define a column for storing the foreign key referencing the "id" column in the "courses" table
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    # Define a relationship with the "Course" model, linking "courses" and "enrolments"
    course = db.relationship('Course', back_populates='enrolments')


class EnrolmentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['id', 'name', 'email'])
    course = fields.Nested('CourseSchema', only=['id', 'title'])
    class Meta:
        fields = ('id', 'user', 'course')
