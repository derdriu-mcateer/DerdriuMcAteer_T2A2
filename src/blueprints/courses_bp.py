from setup import db
from flask import Blueprint, request
from models.course import Course, CourseSchema
from blueprints.auth_bp import admin_required
from flask_jwt_extended import jwt_required
from models.educator import Educator
from blueprints.reviews_bp import reviews_bp


courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

courses_bp.register_blueprint(reviews_bp)


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
        return {"Error": "Course not found"}, 404
    
# Update Course by ID (admin auth required)
@courses_bp.route("/update/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_course(id):
    admin_required()
    # Load course information from the request (JSON format) using CourseSchema
    course_fields = CourseSchema().load(request.json)  
    stmt = db.select(Course).where(Course.id == id)
    course = db.session.scalar(stmt)
    if course:
        course.title = course_fields.get("title", course.title)
        course.date = course_fields.get("date", course.date)
        course.description = course_fields.get("description", course.description)
        course.duration = course_fields.get("duration", course.duration)
        
        # Update the educator if the "educator_id" is provided in the JSON
        educator_id = course_fields.get("educator_id")
        if educator_id:
            educator = Educator.query.get(educator_id)
            if educator:
                course.educator = educator
            else:
                return {"Error": "Invalid Educator ID"}, 400

       
        db.session.commit()
        return CourseSchema().dump(course)
    else:
        return {"Error": "Course not found"}, 404
    

# Delete a Course by ID (admin auth required)
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
        return {"Success": "Course deleted"}, 200
    else: 
        return {"Error": "Course not found"}, 404

# Create a course (admin auth required)
@courses_bp.route("/", methods=["POST"])
@jwt_required()
def create_course():
    admin_required()
    # Load course information from the request (JSON format) using CourseSchema
    course_fields = CourseSchema().load(request.json)  

    educator_id = course_fields.get("educator_id")
    if educator_id:
        educator = Educator.query.get(educator_id)
        if not educator:
            return {"Error": "Invalid Educator ID"}, 400
   
    course = Course(
        title = course_fields["title"],
        date = course_fields["date"],
        description = course_fields["description"],
        duration = course_fields["duration"],
    )

    if educator_id:
        course.educator = educator

    db.session.add(course)  
    db.session.commit()
    return CourseSchema().dump(course)
  


    
