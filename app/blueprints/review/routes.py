from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from app.blueprints.review import bp
from app.blueprints.review.controller import ReviewController

review_controller = ReviewController()


@bp.route('/reviews', methods=['GET'])
def read_reviews():
    return review_controller.read_reviews(request.args)


@bp.route('/reviews/<int:id>', methods=['GET'])
def read_review(id: int):
    try:
        return review_controller.read_review(id)
    except NoResultFound as e:
        return jsonify(e.args[0]), 404


@bp.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    user = get_jwt_identity()

    try:
        return review_controller.create_review(user['id'], request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/reviews/<int:id>', methods=['PUT'])
@jwt_required()
def update_review(id: int):
    user = get_jwt_identity()

    try:
        return review_controller.update_review(id, user['id'], request.json)
    except NoResultFound as e:
        return jsonify(e.args[0]), 404
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/reviews/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id: int):
    user = get_jwt_identity()

    try:
        result = review_controller.delete_review(id, user['id'])
        return jsonify(result)
    except NoResultFound as e:
        return jsonify(e.args[0]), 404
