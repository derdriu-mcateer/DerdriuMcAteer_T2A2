from config import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_or_user
from flask import Blueprint, request
from models.review import Review, ReviewSchema

reviews_bp = Blueprint("reviews", __name__, url_prefix ="/<int:course_id>/reviews")

# Create a new review
@reviews_bp.route("/", methods=['POST'])
@jwt_required()
def new_review(course_id):
    try:
        review_fields = ReviewSchema(only=["description"]).load(request.json)
        review = Review(description = review_fields["description"], user_id=get_jwt_identity(), course_id=course_id)
        db.session.add(review)
        db.session.commit()
        return ReviewSchema().dump(review), 201
    except:
        return {"Error": "Educators cannot create reviews"}, 403
    
# Update a review
@reviews_bp.route("/<int:review_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_review(course_id, review_id):
    review_fields = ReviewSchema(only=["description"]).load(request.json)
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        admin_or_user(review.user_id)
        review.description = review_fields.get("description", review.description)
        db.session.commit()
        return ReviewSchema().dump(review), 200
    else:
        return {"Error": "Review not found"}, 404
    
# Delete a review
@reviews_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(course_id,review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        admin_or_user(review.user_id)
        db.session.delete(review)
        db.session.commit()
        return {"Success": "Review deleted"}, 200
    else:
        return {"Error": "Review not found"}, 404