from setup import db, ma

class Course(db.Model):
    __tablename__= "courses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    duration = db.Column(db.String(), nullable=False)
    capacity = db.Column(db.Integer, default=1)

class CourseSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description")
