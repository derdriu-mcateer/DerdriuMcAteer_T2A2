from setup import db, bcrypt
from models.user import User, UserSchema
from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required, authorize

users_bp = Blueprint("users", __name__, url_prefix="/users")

# View all Users (admin auth required)
@users_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_users():
    admin_required()
    # select all User instances from class User
    stmt = db.select(User)
    # execture the stmt to retrieve scalar users and return them as a list
    users = db.session.scalars(stmt).all()
    # return UserScehma with users converted to JSON format
    return UserSchema(many=True,exclude=["password"]).dump(users)

# View User by ID (admin or user auth required)
@users_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def single_user(id):
    authorize(id)
    # retreive the user from class User based on provided id
    stmt = db.select(User).where(User.id == id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=["password"]).dump(user)
    else:
        return {"error": "User not found"}, 404

# Register new User (no auth required)
@users_bp.route("/register", methods=["POST"])
def user_register():
    # Load user information from the request (JSON format) using UserSchema
    user_fields = UserSchema().load(request.json)
    # Create a new User instance from the loaded JSON information
    user = User(
        email = user_fields["email"],
        password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8"),
    )
    # add instance of User to the database session
    db.session.add(user)
    # Commit session with new instance to the database
    db.session.commit()
    # return new instance of User (excluding password) 
    return UserSchema(exclude=["password"]).dump(user), 201


# Delete User by ID (admin or user auth required)
@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)  
    if user:
        authorize(id)
         # delete the user from the database session
        db.session.delete(user)
        db.session.commit()
        # commit session to the database
        return {"success": "User deleted"}, 200
    else: 
        return {"error": "User not found"}, 404
    
# Update User by ID (admin or user auth required)
@users_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(id):
    # Load user information from the request (JSON format) using UserSchema
    user_fields = UserSchema().load(request.json)  
    stmt = db.select(User).where(User.id == id)
    user = db.session.scalar(stmt)
    if user:
        authorize(id)
        user.email = user_fields.get("email", user.email)
        user.password = user_fields.get("password", user.password)
        user.name = user_fields.get("name", user.name)
        user.phone_number = user_fields.get("phone_number", user.phone_number)
        db.session.commit()
        return UserSchema().dump(user)
    else:
        return {"error": "User not found"}, 404
