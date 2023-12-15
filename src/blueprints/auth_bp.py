from config import db, bcrypt
from models.educator import Educator, EducatorSchema
from models.user import User, UserSchema
from flask import Blueprint, abort, request
from flask_jwt_extended import get_jwt_identity, create_access_token
from datetime import timedelta


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    # EDUCATOR LOGIN 
    educator_fields = EducatorSchema(only=["email", "password"]).load(request.json)
    # Select educator from Educator class where the email matches email parsed in JSON body
    stmt = db.select(Educator).where(Educator.email == educator_fields['email'])
    educator = db.session.scalar(stmt)
    # Check the password entered in JSON body matches password for educator
    if educator and bcrypt.check_password_hash(educator.password, educator_fields["password"]):
        # Create token with email as identity (email used to avoid overlap with user)
        token = create_access_token(identity = educator.email, expires_delta=timedelta(hours=5))
        return {
            "Success": "Educator Login",
            "Educator": EducatorSchema(only=["email"]).dump(educator),
            "token": token  
        }
    
    #USER LOGIN
    user_fields = UserSchema(only=["email", "password"]).load(request.json)
    # Select user from User class where the email matches email parsed in POST body
    stmt = db.select(User).where(User.email == user_fields['email'])
    user = db.session.scalar(stmt)
    # Check the password entered in POST body matches password for user
    if user and bcrypt.check_password_hash(user.password, user_fields["password"]):
        # Create token with id as identity
        token = create_access_token(identity = user.id, expires_delta=timedelta(hours=5))
        return {
            "Success": "User Login",
            "User": UserSchema(only=["email"]).dump(user),
            "token": token
        }
    return {'Error': 'Invalid email address or password'}, 401
    

# Admin only authentication 
def admin_only():
    jwt_id = get_jwt_identity()

    #If id is string (educator) then abort
    if isinstance(jwt_id, str):
            abort(401)
    
    stmt = db.select(User).filter_by(id=jwt_id)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401)

# Admin or current user authentication 
def admin_or_user(id):
    jwt_id = get_jwt_identity()

    #If id is string (educator) then abort
    if isinstance(jwt_id, str):
            abort(401)
    
    user_query = db.select(User).filter_by(id=jwt_id)
    user = db.session.scalar(user_query)
    # If logged in user is neither admin nor user with id matching identity abort
    if not (
        (user and user.is_admin) or (id and (jwt_id == id))
    ):
        abort(401)

# Admin or current educator authentication
def admin_or_educator(id):
    jwt_identity = get_jwt_identity()

    user = None
    educator = None
    # Check if the identity is an integer (User ID)
    if isinstance(jwt_identity, int):  
        user_query = db.select(User).filter_by(id=jwt_identity)
        user = db.session.scalar(user_query)
    else:  # Assume the identity is an email (Educator)
        educator_query = db.select(Educator).filter_by(email=jwt_identity)
        educator = db.session.scalar(educator_query)
    # If logged in user is neither admin nor educator with id matching identity then abort
    if not (
        (user and user.is_admin) or (educator and (educator.id == id))
    ):
        abort(401)






