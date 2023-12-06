from setup import db, ma


class UserCourse(db.Model):
    __tablename__ = "user_courses"
    
    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    course = db.relationship("Course", back_populates="user_course")
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="user_course")
    
    

class UserCourseSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("course_id", "user_id")

