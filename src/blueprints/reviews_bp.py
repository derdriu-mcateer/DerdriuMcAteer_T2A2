from setup import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request


from models.review import Review, ReviewSchema

reviews_bp = Blueprint("reviews", __name__, url_prefix="/<int:course_id>/reviews")

# Create a new review
@reviews_bp.route("/", methods=['POST'])
@jwt_required()
def new_review(course_id):
    review_fields = ReviewSchema(only=["description"]).load(request.json)
    review = Review(description = review_fields["description"], user_id=get_jwt_identity(), course_id=course_id)
    db.session.add(review)
    db.session.commit()
    return ReviewSchema().dump(review), 201