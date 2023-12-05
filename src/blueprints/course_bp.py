from setup import db
from flask import Blueprint
from models.course import Course, CourseSchema
from flask_jwt_extended import jwt_required


courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

@courses_bp.route("/", methods=["GET"])
@jwt_required()
def get_courses():
    stmt = db.select(Course)
    courses = db.session.scalars(stmt).all()
    return CourseSchema(many=True).dump(courses)