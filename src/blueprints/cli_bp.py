from config import db, bcrypt
from flask import Blueprint
from models.course import Course
from models.educator import Educator
from models.user import User
from models.enrolment import Enrolment
from models.review import Review
from datetime import date


db_commands = Blueprint('db', __name__)

# db create will drop all existing tables and create new database tables based on defined models
@db_commands.cli.command("create")
def create_db():
    # Drop existing database tables
    db.drop_all()
    # Create new database tables
    db.create_all()
    print("Success: Tables created")

# db seed will add data into the database tables
@db_commands.cli.command("seed")
def seed_db():
        # create instances of educators
    educators = [
        Educator(
            email="educator1@example.com",
            password=bcrypt.generate_password_hash("Password1").decode("utf8"),
            name="Gabriella Ramirez",
            d_o_b=date(1985, 10, 25),
            phone_number="1234567890",
            
        ),

        Educator(
            email="educator2@example.com",
            password=bcrypt.generate_password_hash("Password2").decode("utf8"),
            name="Declan Patel",
            d_o_b=date(1978, 7, 15),
            phone_number="9876543210",
            
        ),

        Educator(
            email="educator3@example.com",
            password=bcrypt.generate_password_hash("Password3").decode("utf8"),
            name="Emilia Nguyen",
            d_o_b=date(1990, 4, 5),
            phone_number="5551234567",
            
        ),

        Educator(
            email="educator4@example.com",
            password=bcrypt.generate_password_hash("Password4").decode("utf8"),
            name="Kaleb Johnston",
            d_o_b=date(1983, 1, 12),
            phone_number="9998887776",
            
        ),

        Educator(
            email="educator5@example.com",
            password=bcrypt.generate_password_hash("Password5").decode("utf8"),
            name="Isla Rodriguez",
            d_o_b=date(1995, 12, 30),
            phone_number="4443332221",
            
        )
    ]
    # add all instances of educators to the session 
    db.session.add_all(educators)
    db.session.commit()

    # create instances of courses
    courses = [
        Course(
            title="Mindfulness Meditation",
            description="Learn mindfulness techniques for stress relief and mental well-being.",
            duration="3 hours",
            educator_id = educators[0].id
        ),

        Course(
            title="Effective Communication Skills",
            description="Develop effective communication skills for personal and professional growth.",
            duration="8 hours",
            educator_id = educators[2].id
        ),

        Course(
            title="Time Management Mastery",
            description="Master the art of time management and productivity.",
            duration="2 hours",
            educator_id = educators[4].id
        ),

        Course(
            title="Emotional Intelligence Training",
            description="Enhance emotional intelligence and self-awareness for better relationships.",
            duration="6 hours",
            educator_id = educators[2].id
        ),

        Course(
            title="Goal Setting and Achievement",
            description="Learn strategies to set and achieve personal and professional goals.",
            duration="6 hours",
            educator_id = educators[1].id
        ),

        Course(
            title="Stress Management Techniques",
            description="Explore stress management techniques for a balanced lifestyle.",
            duration="2 hours",
            educator_id = educators[0].id
        )
    ]
    # add all instances of courses to the session 
    db.session.add_all(courses)
    db.session.commit()

    # create instances of users
    users = [
        User(
            email="user1@example.com",
            password=bcrypt.generate_password_hash("Password1").decode("utf8"),
            name="Elise Chen",
            d_o_b=date(1990, 5, 15),
            phone_number="1234567890",
            is_admin=True
        ),

        User(
            email="user2@example.com",
            password=bcrypt.generate_password_hash("Password2").decode("utf8"),
            name="Nico Foster",
            d_o_b=date(1988, 9, 20),
            phone_number="9876543210",
            is_admin=False
        ),

        User(
            email="user3@example.com",
            password=bcrypt.generate_password_hash("Password3").decode("utf8"),
            name="Asher Martinez",
            d_o_b=date(1995, 3, 8),
            phone_number="5551234567",
            is_admin=True
        ),

        User(
            email="user4@example.com",
            password=bcrypt.generate_password_hash("Password4").decode("utf8"),
            name="Owen Sullivan",
            d_o_b=date(1983, 7, 12),
            phone_number="9998887776",
            is_admin=False
        ),

        User(
            email="user5@example.com",
            password=bcrypt.generate_password_hash("Password5").decode("utf8"),
            name="Sophia Lee",
            d_o_b=date(1998, 11, 25),
            phone_number="4443332221",
            is_admin=False
        ),

        User(
            email="user6@example.com",
            password=bcrypt.generate_password_hash("Password6").decode("utf8"),
            name="Oliver Wilson",
            d_o_b=date(1980, 12, 30),
            phone_number="7779991110",
            is_admin=False
        )
    ]
    # add all instances of users to the session 
    db.session.add_all(users)
    db.session.commit()

    enrolments = [
        # create instances of enrolments
        Enrolment(
            course_id = courses[1].id,
            user_id= users[0].id
        ),

        Enrolment(
            course_id = courses[3].id,
            user_id= users[0].id
        ),

        Enrolment(
            course_id = courses[5].id,
            user_id= users[2].id
        ),

        Enrolment(
            course_id = courses[4].id,
            user_id= users[3].id
        ),
    ]
    # add all instances of enrolments to the session 
    db.session.add_all(enrolments)
    db.session.commit()

    reviews = [
        # create instances of reviews
    Review(
        description="This course was great",
        course_id=courses[0].id,
        user_id=users[0].id
    ),
    Review(
        description="The content was really helpful",
        course_id=courses[1].id,
        user_id=users[1].id
    ),
    Review(
        description="Enjoyed the practical exercises",
        course_id=courses[2].id,
        user_id=users[2].id
    ),
    Review(
        description="The instructor was fantastic",
        course_id=courses[3].id,
        user_id=users[3].id
    ),
    Review(
        description="Highly recommended!",
        course_id=courses[4].id,
        user_id=users[4].id
    ),
    Review(
        description="Loved the interactive sessions",
        course_id=courses[5].id,
        user_id=users[1].id
    )
    ]
    # add all instances of reviews to the session 
    db.session.add_all(reviews)
    db.session.commit()

    print("Success: Table seeded")
