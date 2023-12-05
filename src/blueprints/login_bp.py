from setup import db, bcrypt
from models.educator import Educator, EducatorSchema
from models.user import User, UserSchema
from flask import request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta
from flask import Blueprint



login_bp = Blueprint("logins", __name__, url_prefix="/login")

@login_bp.route("/", methods=["POST"])
def login():
    educator_fields = EducatorSchema(only=["email", "password"]).load(request.json)
    stmt = db.select(Educator).where(Educator.email == educator_fields['email'])
    educator = db.session.scalar(stmt)
    if educator and bcrypt.check_password_hash(educator.password, educator_fields["password"]):
        token = create_access_token(identity = str(educator.email), expires_delta=timedelta(hours=5))
        return {
            "Success": "Educator Login",
            "user": EducatorSchema(only=["id","email"]).dump(educator),
            "token": token  
        }
    
    user_fields = UserSchema(only=["email", "password"]).load(request.json)
    stmt = db.select(User).where(User.email == user_fields['email'])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, user_fields["password"]):
        token = create_access_token(identity = str(user.email), expires_delta=timedelta(hours=5))
        return {
            "Success": "User Login",
            "user": UserSchema(only=["id","email"]).dump(user),
            "token": token  
        }
    else:
        return {"error": "Invalid email or password"}, 401
    
def admin_required():
    jwt_educator_id = get_jwt_identity()
    stmt = db.select(Educator).filter_by(email=jwt_educator_id)
    educator = db.session.scalar(stmt)
    if not (educator and educator.is_admin):
        abort(401)
    print(jwt_educator_id)