from setup import db
from models.educator import Educator
from models.user import User
from flask import abort
from flask_jwt_extended import get_jwt_identity
from flask import Blueprint



auth_bp = Blueprint("logins", __name__, url_prefix="/login")

def admin_required():
    jwt_user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401)

def admin_or_user(id):
    jwt_id = get_jwt_identity()

    user_query = db.select(User).filter_by(id=jwt_id)
    user = db.session.scalar(user_query)

    if not (
        (user and user.is_admin) or 
        (id and (jwt_id == id))
    ):
        abort(401)

def admin_or_educator(id):
    jwt_identity = get_jwt_identity()

    user = None
    educator = None
 
    if isinstance(jwt_identity, int):  # Check if the identity is an integer (User ID)
        user_query = db.select(User).filter_by(id=jwt_identity)
        user = db.session.scalar(user_query)
    else:  # Assume the identity is an email (Educator)
        educator_query = db.select(Educator).filter_by(email=jwt_identity)
        educator = db.session.scalar(educator_query)

    if not (
        (user and user.is_admin) or 
        (educator and (educator.id == id))
    ):
        abort(401)






