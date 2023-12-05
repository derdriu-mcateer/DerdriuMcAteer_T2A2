from setup import db
from flask import Blueprint
from models.course import Course, CourseSchema
from blueprints.login_bp import admin_required
from flask_jwt_extended import jwt_required


courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

# View all Courses
@courses_bp.route("/", methods=["GET"])
@jwt_required()
def get_courses():
    stmt = db.select(Course)
    courses = db.session.scalars(stmt).all()
    return CourseSchema(many=True).dump(courses)

# View Course by ID 
@courses_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def single_course(id):
    stmt = db.select(Course).where(Course.id == id)
    course = db.session.scalar(stmt)
    if course:
        return CourseSchema().dump(course)
    else: 
        return {"error": "Course not found"}, 404
    

# Delete a Course by ID (admins only)
@courses_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_course(id):
    admin_required()
    stmt = db.select(Course).where(Course.id == id)
    course = db.session.scalar(stmt)
    if course:
        db.session.delete(course)
        db.session.commit()
        return {"success": "Course deleted"}, 200
    else: 
        return {"error": "Course not found"}, 404



    
