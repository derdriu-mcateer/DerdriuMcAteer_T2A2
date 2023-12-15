from config import db, bcrypt
from models.user import User, UserSchema
from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_only, admin_or_user
from blueprints.enrolments_bp import enrolments_bp

users_bp = Blueprint("users", __name__, url_prefix="/users")

users_bp.register_blueprint(enrolments_bp)

# View all Users (admin auth required)
@users_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_users():
    admin_only()
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
    admin_or_user(id)
    # retreive the user from class User based on provided id
    stmt = db.select(User).where(User.id == id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=["password"]).dump(user)
    else:
        return {"Error": "User not found"}, 404

# Register new User (no auth required)
@users_bp.route("/register", methods=["POST"])
def user_register():
    # Load user information from the request (JSON format) using UserSchema
    user_fields = UserSchema().load(request.json)
    # Create a new User instance from the loaded JSON information
    user = User(
        email = user_fields["email"],
        password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8"),
        name = user_fields["name"],
        d_o_b = user_fields["d_o_b"],
        phone_number = user_fields["phone_number"],
    )
    # add instance of User to the database session
    db.session.add(user)
    # Commit session with new instance to the database
    db.session.commit()
    # return new instance of User (excluding password) 
    return UserSchema(exclude=["password", "is_admin", "enrolments", "reviews"]).dump(user), 201


# Delete User by ID (admin or user auth required)
@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    admin_or_user(id)
    user = User.query.get(id)  
    if user:
         # delete the user from the database session
        db.session.delete(user)
        db.session.commit()
        # commit session to the database
        return {"Success": "User deleted"}, 200
    else: 
        return {"Error": "User not found"}, 404
    
# Update User by ID (admin or user auth required)
@users_bp.route("/<int:id>/update", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(id):
    admin_or_user(id)
    # Load user information from the request (JSON format) using UserSchema
    user_fields = UserSchema(partial=True).load(request.json) 
    # Retrieve the user by user_id 
    stmt = db.select(User).where(User.id == id)
    user = db.session.scalar(stmt)
    if user:
        user.email = user_fields.get("email", user.email)
        user.name = user_fields.get("name", user.name)
        user.phone_number = user_fields.get("phone_number", user.phone_number)
        user.d_o_b = user_fields.get("d_o_b", user.d_o_b)

        current_user_id = get_jwt_identity()
        # Only user associated with the account can update the password
        if user_fields.get("password"):
            if current_user_id == id:
                user.password = bcrypt.generate_password_hash(user_fields.get("password")).decode("utf-8")
            else:
                return {"error": "Only the user associated with this account can update the password"}, 403
        db.session.commit()
        return UserSchema(exclude=["password"]).dump(user), 200
    else:
        return {"Error": "User not found"}, 404
    
# Update admin status of a user (admin auth required)
@users_bp.route("/<int:id>/update_admin", methods=["PUT", "PATCH"])
@jwt_required()
def update_user_admin_status(id):
    admin_only()
    # Retrieve the user by user_id
    user_fields = UserSchema().load(request.json)  
    stmt = db.select(User).where(User.id == id)
    user = db.session.scalar(stmt)
    
    if user:
        # Update the is_admin status based on the request data
        new_admin = user_fields.get("is_admin")
        if new_admin is not None:
            user.is_admin = new_admin
            db.session.commit()
            return UserSchema(exclude=["password"]).dump(user), 200
        else:
            return {"Error": "Invalid request. 'is_admin' field not provided."}, 400
    else:
        return {"Error": "User not found"}, 404
    
