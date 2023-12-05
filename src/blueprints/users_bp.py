from setup import db, bcrypt
from models.user import User, UserSchema
from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from blueprints.login_bp import admin_required

users_bp = Blueprint("users", __name__, url_prefix="/users")

# View all Users 
@users_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True).dump(users)

# View User by ID
@users_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def single_user(id):
    stmt = db.select(User).where(User.id == id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=["password"]).dump(user)
    else:
        return {"error": "User not found"}, 404

# Register new User 
@users_bp.route("/register", methods=["POST"])
def user_register():
    user_fields = UserSchema().load(request.json)
    user = User(
        email = user_fields["email"],
        password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8"),
    )
    db.session.add(user)
    db.session.commit()

    return UserSchema(exclude=["password"]).dump(user), 201


# Delete Educator by ID
@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    admin_required()
    stmt = db.select(User).where(User.id == id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {"success": "User deleted"}, 200
    else: 
        return {"error": "User not found"}, 404