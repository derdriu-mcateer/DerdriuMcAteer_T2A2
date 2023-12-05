from setup import db, bcrypt
from flask import Blueprint
from models.course import Course
from models.educator import Educator
from models.user import User
from datetime import date

db_commands = Blueprint('db', __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("seed")
def seed_db():
    
    courses = [
# Example instances of the Course model focusing on personal development
        Course(
            title="Mindfulness Meditation",
            description="Learn mindfulness techniques for stress relief and mental well-being.",
            duration="3 hours",
            capacity=50
        ),

        Course(
            title="Effective Communication Skills",
            description="Develop effective communication skills for personal and professional growth.",
            duration="8 hours",
            capacity=30
        ),

        Course(
            title="Time Management Mastery",
            description="Master the art of time management and productivity.",
            duration="2 hours",
            capacity=40
        ),

        Course(
            title="Emotional Intelligence Training",
            description="Enhance emotional intelligence and self-awareness for better relationships.",
            duration="6 hours",
            capacity=25
        ),

        Course(
            title="Goal Setting and Achievement",
            description="Learn strategies to set and achieve personal and professional goals.",
            duration="6 hours",
            capacity=35
        ),

        Course(
            title="Stress Management Techniques",
            description="Explore stress management techniques for a balanced lifestyle.",
            duration="2 hours",
            capacity=20
        )

    ]
    db.session.add_all(courses)

    educators = [
        Educator(
            email="educator1@example.com",
            password=bcrypt.generate_password_hash("password1").decode("utf8"),
            name="Gabriella Ramirez",
            d_o_b=date(1985, 10, 25),
            phone_number="1234567890",
            is_admin=True
        ),

        Educator(
            email="educator2@example.com",
            password=bcrypt.generate_password_hash("password2").decode("utf8"),
            name="Declan Patel",
            d_o_b=date(1978, 7, 15),
            phone_number="9876543210",
            is_admin=False
        ),

        Educator(
            email="educator3@example.com",
            password=bcrypt.generate_password_hash("password3").decode("utf8"),
            name="Emilia Nguyen",
            d_o_b=date(1990, 4, 5),
            phone_number="5551234567",
            is_admin=False
        ),

        Educator(
            email="educator4@example.com",
            password=bcrypt.generate_password_hash("password4").decode("utf8"),
            name="Kaleb Johnston",
            d_o_b=date(1983, 1, 12),
            phone_number="9998887776",
            is_admin=True
        ),

        Educator(
            email="educator5@example.com",
            password=bcrypt.generate_password_hash("password5").decode("utf8"),
            name="Isla Rodriguez",
            d_o_b=date(1995, 12, 30),
            phone_number="4443332221",
            is_admin=False
        )
    ]
    db.session.add_all(educators)

    users = [
        User(
            email="user1@example.com",
            password=bcrypt.generate_password_hash("password1").decode("utf8"),
            name="Elise Chen",
            d_o_b=date(1990, 5, 15),
            phone_number="1234567890"
        ),

        User(
            email="user2@example.com",
            password=bcrypt.generate_password_hash("password2").decode("utf8"),
            name="Nico Foster",
            d_o_b=date(1988, 9, 20),
            phone_number="9876543210"
        ),

        User(
            email="user3@example.com",
            password=bcrypt.generate_password_hash("password3").decode("utf8"),
            name="Asher Martinez",
            d_o_b=date(1995, 3, 8),
            phone_number="5551234567"
        ),

        User(
            email="user4@example.com",
            password=bcrypt.generate_password_hash("password4").decode("utf8"),
            name="Owen Sullivan",
            d_o_b=date(1983, 7, 12),
            phone_number="9998887776"
        ),

        User(
            email="user5@example.com",
            password=bcrypt.generate_password_hash("password5").decode("utf8"),
            name="Sophia Lee",
            d_o_b=date(1998, 11, 25),
            phone_number="4443332221"
        ),

        User(
            email="user6@example.com",
            password=bcrypt.generate_password_hash("password6").decode("utf8"),
            name="Oliver Wilson",
            d_o_b=date(1980, 12, 30),
            phone_number="7779991110"
        )
    ]
    db.session.add_all(users)
    
    db.session.commit()
    print("Table seeded")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")