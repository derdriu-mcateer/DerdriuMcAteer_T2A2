from setup import db
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.course import Course
from models.enrolment import Enrolment


enrolments_bp = Blueprint("enrolments", __name__, url_prefix="/enrolments")

# Enrol User into Course
@enrolments_bp.route("/enrol/<int:course_id>", methods=["PUT"])
@jwt_required()
def enrol_user(course_id):
    # Get the current user's ID from the JWT token
    current_user_email = str(get_jwt_identity())

    # Check if the user exists and retrieve the user object
    user = User.query.filter_by(email=current_user_email).first()
    if user is None:
        return {"error": "User not found"}, 404

    # Retrieve the course from the provided course_id
    course = Course.query.get(course_id)
    if course is None:
        return {"error": "Course not found"}, 404
    
    if Enrolment.query.filter_by(user=user, course=course).first():
        return {"error": "User already enrolled in the course"}, 400

    # Create an Enrolment object and associate it with the user and course
    enrolment = Enrolment(user=user, course=course)
    db.session.add(enrolment)
    db.session.commit()

    return {"success": "User enrolled in the course"}, 200

@enrolments_bp.route("/unenrol/<int:course_id>", methods=["DELETE"])
@jwt_required()
def unenrol_user(course_id):
    # Get the current user's email from the JWT token
    current_user_email = str(get_jwt_identity())
    
    # Check if the user exists and retrieve the user object
    user = User.query.filter_by(email=current_user_email).first()
    if user is None:
        return {"error": "User not found"}, 404

    # Retrieve the course from the provided course_id
    course = Course.query.get(course_id)
    if course is None:
        return {"error": "Course not found"}, 404

    # Find the specific enrollment record for the user and course
    enrollment = Enrolment.query.filter_by(user=user, course=course).first()
    if enrollment is None:
        return {"error": "User is not enrolled in the course"}, 400

    # Delete the enrollment record
    db.session.delete(enrollment)
    db.session.commit()

    return {"success": "User unenrolled from the course"}, 200