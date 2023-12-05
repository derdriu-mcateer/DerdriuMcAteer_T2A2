from setup import db, bcrypt
from models.educator import Educator, EducatorSchema
from blueprints.login_bp import admin_required
from flask import request, Blueprint
from flask_jwt_extended import jwt_required


educators_bp = Blueprint("educators", __name__, url_prefix="/educators")

# View all Educators 
@educators_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_educators():
    stmt = db.select(Educator)
    educators = db.session.scalars(stmt).all()
    return EducatorSchema(many=True).dump(educators)

# View Educator by ID
@educators_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def single_educator(id):
    stmt = db.select(Educator).where(Educator.id == id)
    educator = db.session.scalar(stmt)
    if educator:
        return EducatorSchema(exclude=["password"]).dump(educator)
    else:
        return {"error": "Educator not found"}, 404

# Register new Educator
@educators_bp.route("/register", methods=["POST"])
@jwt_required()
def educator_register():
    admin_required()
    educator_fields = EducatorSchema().load(request.json)
    educator = Educator(
        email = educator_fields["email"],
        password = bcrypt.generate_password_hash(educator_fields["password"]).decode("utf-8"),
        is_admin = educator_fields["is_admin"]
    )
    db.session.add(educator)
    db.session.commit()

    return EducatorSchema(exclude=["password"]).dump(educator), 201




