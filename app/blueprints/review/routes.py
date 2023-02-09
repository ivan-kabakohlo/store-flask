from flask import jsonify, request
from marshmallow import ValidationError

from app.blueprints.product import bp
from app.repositories.review import review_repository


@bp.route('/reviews', methods=['GET'])
def read_reviews():
    product_id = request.args.get('product_id', '')
    author_id = request.args.get('author_id', '')

    product_id = int(product_id) if product_id.isdigit() else None
    author_id = int(author_id) if author_id.isdigit() else None

    return review_repository.read_all(product_id, author_id)


@bp.route('/reviews/<int:id>', methods=['GET'])
def read_review(id: int):
    return review_repository.read_by_id(id)


@bp.route('/reviews', methods=['POST'])
def create_review():
    try:
        return review_repository.create(request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/reviews/<int:id>', methods=['PUT'])
def update_review(id: int):
    try:
        return review_repository.update_by_id(id, request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id: int):
    review_repository.delete_by_id(id)
    return jsonify({'message': 'Deleted'})
