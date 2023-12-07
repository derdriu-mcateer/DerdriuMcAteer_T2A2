from setup import db, ma
from marshmallow import fields

# Course class inherits from db.Model allowing it to map objects to corresponding db tables
class Course(db.Model):
    # define the table name for the database
    __tablename__= "courses"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    duration = db.Column(db.String(), nullable=False)
    capacity = db.Column(db.Integer, default=1)

    educator_id = db.Column(db.Integer, db.ForeignKey("educators.id"),nullable=False)
    educator = db.relationship("Educator", back_populates="courses", cascade="all, delete")

    enrolments = db.relationship('Enrolment', back_populates='course', cascade='all, delete')

    reviews = db.relationship('Review', back_populates='course', cascade='all, delete')

# Create the CourseSchema with marshmallow 
class CourseSchema(ma.Schema):
    educator = fields.Nested('EducatorSchema', only=('id', 'name', 'email'))
    enrolments = fields.Nested('EnrolmentSchema', many=True, only=['user'])
    reviews = fields.Nested('ReviewSchema', many=True,exclude=['course'])

    class Meta:
        ordered = True
        fields = ("id", "title",  "description", "duration", "capacity", "educator", 'enrolments', "reviews")