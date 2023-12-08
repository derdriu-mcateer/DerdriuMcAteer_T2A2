from setup import db, bcrypt
from models.educator import Educator, EducatorSchema
from models.user import User, UserSchema
from blueprints.educators_bp import educators_bp
from blueprints.users_bp import users_bp
from flask import request
from flask_jwt_extended import create_access_token
from datetime import timedelta
from flask import Blueprint

login_bp = Blueprint('auth', __name__)

@educators_bp.route("/login", methods=['POST'])
# EDUCATOR LOGIN
def educator_login():
    try: 
        # Parse incoming POST data through the schema
        educator_fields = EducatorSchema(only=["email", "password"]).load(request.json)
        # Select educator from Educator class where the email matches email parsed in POST body
        stmt = db.select(Educator).where(Educator.email == educator_fields['email'])
        educator = db.session.scalar(stmt)
        # Check the password entered in POST body matches password for educator
        if educator and bcrypt.check_password_hash(educator.password, educator_fields["password"]):
            # Create token with email as identity
            token = create_access_token(identity = educator.email, expires_delta=timedelta(hours=5))
            return {
                "Success": "Educator Login",
                "Educator": EducatorSchema(only=["email"]).dump(educator),
                "token": token  
            }
    except KeyError:
        return {"error": "Email and passsword are required"}, 400
    
@users_bp.route("/login", methods=["POST"])
#USER LOGIN
def user_login():
    try:
        user_fields = UserSchema(only=["email", "password"]).load(request.json)
        # Select user from User class where the email matches email parsed in POST body
        stmt = db.select(User).where(User.email == user_fields['email'])
        user = db.session.scalar(stmt)
        # Check the password entered in POST body matches password for user
        if user and bcrypt.check_password_hash(user.password, user_fields["password"]):
            # Create token with email as identity
            token = create_access_token(identity = user.id, expires_delta=timedelta(hours=5))
            return {
                "Success": "User Login",
                "User": UserSchema(only=["email"]).dump(user),
                "token": token
            }
        return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {"error": "Email and passsword are required"}, 400
    

