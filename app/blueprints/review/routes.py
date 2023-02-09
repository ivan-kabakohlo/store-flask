from flask import jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.blueprints.review import bp
from app.blueprints.review.controller import ReviewController

review_controller = ReviewController()


@bp.route('/reviews', methods=['GET'])
def read_reviews():
    return review_controller.read_reviews(request.args)


@bp.route('/reviews/<int:id>', methods=['GET'])
def read_review(id: int):
    return review_controller.read_review(id)


@bp.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    try:
        return review_controller.create_review(request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/reviews/<int:id>', methods=['PUT'])
@jwt_required()
def update_review(id: int):
    try:
        return review_controller.update_review(id, request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/reviews/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id: int):
    result = review_controller.delete_review(id)
    return jsonify(result)
