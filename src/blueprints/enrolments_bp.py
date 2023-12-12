from config import db
from flask import Blueprint
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_or_user
from models.user import User
from models.course import Course
from models.enrolment import Enrolment


enrolments_bp = Blueprint("enrolments", __name__, url_prefix="/<int:user_id>/enrolments")

# Enrol User into Course
@enrolments_bp.route("<int:course_id>", methods=["POST"])
@jwt_required()
def enrol_user(course_id, user_id):
    admin_or_user(user_id)
    # Check if the user exists and retrieve the user object
    user = User.query.get(user_id)
    if user is None:
        return {"Error": "User not found"}, 404

    # Retrieve the course from the provided course_id
    course = Course.query.get(course_id)
    if course is None:
        return {"Error": "Course not found"}, 404
    
    if course.capacity:
        current_capacity = len(course.enrolments)
        if current_capacity >= course.capacity:
            return {"Error": "This course is full."}, 400
    
    if Enrolment.query.filter_by(user=user, course=course).first():
        return {"Error": "User already enrolled in the course"}, 400
    

    # Create an Enrolment object and associate it with the user and course
    enrolment = Enrolment(user=user, course=course)
    db.session.add(enrolment)
    db.session.commit()

    return {"Success": "User enrolled in the course"}, 201

# Unenrol User into Course
@enrolments_bp.route("<int:course_id>", methods=["DELETE"])
@jwt_required()
def unenrol_user(course_id, user_id):
    admin_or_user(user_id)
    # Check if the user exists and retrieve the user object
    user = User.query.get(user_id)
    if user is None:
        return {"Error": "User not found"}, 404

    # Retrieve the course from the provided course_id
    course = Course.query.get(course_id)
    if course is None:
        return {"Error": "Course not found"}, 404

    # Find the specific enrollment record for the user and course
    enrollment = Enrolment.query.filter_by(user=user, course=course).first()
    if enrollment is None:
        return {"Error": "User is not enrolled in the course"}, 400

    # Delete the enrollment record
    db.session.delete(enrollment)
    db.session.commit()

    return {"Success": "User unenrolled from the course"}, 200