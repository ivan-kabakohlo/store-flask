from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from app.blueprints.review import bp
from app.blueprints.review.controller import ReviewController

review_controller = ReviewController()


@bp.route('/reviews', methods=['GET'])
def read_review_list():
    return review_controller.read_review_list(filters=request.args)


@bp.route('/reviews/<int:id>', methods=['GET'])
def read_review(id: int):
    try:
        return review_controller.read_review(id=id)
    except NoResultFound:
        return jsonify({'message': 'Review not found'}), 404


@bp.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    user = get_jwt_identity()

    try:
        return review_controller.create_review(
            user_id=user['id'], body=request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/reviews/<int:id>', methods=['PUT'])
@jwt_required()
def update_review(id: int):
    user = get_jwt_identity()

    try:
        return review_controller.update_review(
            id=id, user_id=user['id'], body=request.json)
    except NoResultFound:
        return jsonify({'message': 'Review not found'}), 404
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/reviews/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id: int):
    user = get_jwt_identity()

    try:
        result = review_controller.delete_review(id=id, user_id=user['id'])
        return jsonify(result)
    except NoResultFound:
        return jsonify({'message': 'Review not found'}), 404
