from setup import db, ma
from marshmallow import fields


class Enrolment(db.Model):
    __tablename__ = 'enrolments'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='enrolments')

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('Course', back_populates='enrolments')


class EnrolmentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['id', 'name', 'email'])
    course = fields.Nested('CourseSchema', only=['id', 'title'])
    class Meta:
        fields = ('id', 'user', 'course')
