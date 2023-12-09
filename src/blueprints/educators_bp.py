from setup import db, bcrypt
from models.educator import Educator, EducatorSchema
from blueprints.auth_bp import admin_required, admin_or_educator
from flask import request, Blueprint
from flask_jwt_extended import jwt_required


educators_bp = Blueprint("educators", __name__, url_prefix="/educators")

# View all Educators (admin auth required)
@educators_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_educators():
    admin_required()
    # select all educator instances from class Educator
    stmt = db.select(Educator)
    # execture the stmt to retrieve scalar educators and return them as a list
    educators = db.session.scalars(stmt).all()
    # return EducatorScehma with educators converted to JSON format
    return EducatorSchema(many=True, exclude=["password"]).dump(educators)

# View Educator by ID (admin auth required)
@educators_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def single_educator(id):
    admin_or_educator(id)
    # retreive the educator from class Educator based on provided id
    stmt = db.select(Educator).where(Educator.id == id)
    educator = db.session.scalar(stmt)
    if educator:
        return EducatorSchema(exclude=["password"]).dump(educator)
    else:
        return {"error": "Educator not found"}, 404

# Register new Educator (admins auth required)
@educators_bp.route("/register", methods=["POST"])
@jwt_required()
def educator_register():
    admin_required()
    # Load educator information from the request (JSON format) using EducatorSchema
    educator_fields = EducatorSchema().load(request.json)
    # Create a new Educator instance from the loaded JSON information
    educator = Educator(
        email = educator_fields["email"],
        password = bcrypt.generate_password_hash(educator_fields["password"]).decode("utf-8"),
        name = educator_fields["name"],
        d_o_b = educator_fields["d_o_b"],
        phone_number = educator_fields["phone_number"]
    )
    # add instance of Educator to the database session
    db.session.add(educator)
    # Commit session with new instance to the database
    db.session.commit()
    # return new instance of Educator (excluding password)
    return EducatorSchema(exclude=["password"]).dump(educator), 201

# Delete Educator by ID (admins auth required)
@educators_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_educator(id):
    admin_required()
    stmt = db.select(Educator).where(Educator.id == id)
    educator = db.session.scalar(stmt)
    if educator:
        # delete the educator from the database session
        db.session.delete(educator)
        # commit session to the database
        db.session.commit()
        return {"success": "Educator deleted"}, 200
    else: 
        return {"error": "Educator not found"}, 404


@educators_bp.route("/update/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_educator(id):
    admin_or_educator(id)
    # Load educator information from the request (JSON format) using UserSchema
    educator_fields = EducatorSchema().load(request.json)  
    stmt = db.select(Educator).where(Educator.id == id)
    educator = db.session.scalar(stmt)
    if educator:
        educator.email = educator_fields.get("email", educator.email)
        educator.password = educator_fields.get("password", educator.password)
        educator.name = educator_fields.get("name", educator.name)
        educator.phone_number = educator_fields.get("phone_number", educator.phone_number)
        educator.d_o_b = educator_fields.get("d_o_b", educator.d_o_b)
        db.session.commit()
        return EducatorSchema(exclude=["password"]).dump(educator)
    else:
        return {"error": "Educator not found"}, 404


