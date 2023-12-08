from setup import db, bcrypt
from models.educator import Educator, EducatorSchema
from models.user import User, UserSchema
from flask import request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta
from flask import Blueprint



login_bp = Blueprint("logins", __name__, url_prefix="/login")

# Allow users and educators to login 
@login_bp.route("/", methods=["POST"])
def login():
    try:
        # EDUCATOR LOGIN 
        # Parse incoming POST data through the schema
        educator_fields = EducatorSchema(only=["email", "password"]).load(request.json)
        # Select educator from Educator class where the email matches email parsed in POST body
        stmt = db.select(Educator).where(Educator.email == educator_fields['email'])
        educator = db.session.scalar(stmt)
        # Check the password entered in POST body matches password for educator
        if educator and bcrypt.check_password_hash(educator.password, educator_fields["password"]):
            # Create token with email as identity
            token = create_access_token(identity = str(educator.email), expires_delta=timedelta(hours=5))
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
            # Create token with email as identity
            token = create_access_token(identity = str(user.email), expires_delta=timedelta(hours=5))
            return {
                "Success": "User Login",
                "User": UserSchema(only=["email"]).dump(user),
                "token": token
            }
        return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {"error": "Email and passsword are required"}, 400

 
def admin_required():
    jwt_educator_id = get_jwt_identity()
    stmt = db.select(Educator).filter_by(email=jwt_educator_id)
    educator = db.session.scalar(stmt)
    if not (educator and educator.is_admin):
        abort(401)


def authorize(identity):
    jwt_id = get_jwt_identity()

    user_query = db.select(User).filter_by(email=jwt_id)
    educator_query = db.select(Educator).filter_by(email=jwt_id)

    user = db.session.scalar(user_query)
    educator = db.session.scalar(educator_query)

    if not ((educator and educator.is_admin) or (user and (user.id == identity))):
        abort(401)




