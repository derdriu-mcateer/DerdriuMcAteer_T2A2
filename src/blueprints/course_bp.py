from setup import db
from flask import Blueprint
from models.course import Course, CourseSchema
from blueprints.login_bp import admin_required
from flask_jwt_extended import jwt_required


courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

# View all Courses (auth required)
@courses_bp.route("/", methods=["GET"])
@jwt_required()
def get_courses():
    # select all course entries from class Course
    stmt = db.select(Course)
    # execture the stmt to retrieve scalar courses and return them as a list
    courses = db.session.scalars(stmt).all()
    # return CourseSchema with courses converted to JSON format
    return CourseSchema(many=True).dump(courses)

# View Course by ID (auth required)
@courses_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def single_course(id):
    # retreive the course from class Course based on provided id
    stmt = db.select(Course).where(Course.id == id)
    course = db.session.scalar(stmt)
    if course:
        return CourseSchema().dump(course)
    else: 
        return {"error": "Course not found"}, 404
    

# Delete a Course by ID (admins auth required)
@courses_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_course(id):
    admin_required()
    stmt = db.select(Course).where(Course.id == id)
    course = db.session.scalar(stmt)
    if course:
        # delete the course from the database session
        db.session.delete(course)
        # commit session to the database
        db.session.commit()
        return {"success": "Course deleted"}, 200
    else: 
        return {"error": "Course not found"}, 404



    
