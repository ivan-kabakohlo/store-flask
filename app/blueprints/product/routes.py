from flask import jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.blueprints.product import bp
from app.repositories.product import product_repository


@bp.route('/products', methods=['GET'])
def read_product_list():
    return product_repository.read_all()


@bp.route('/products/<int:id>', methods=['GET'])
def read_product(id: int):
    return product_repository.read_by_id(id)


@bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    try:
        return product_repository.create(request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id: int):
    try:
        return product_repository.update_by_id(id, request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id: int):
    product_repository.delete_by_id(id)
    return jsonify({'message': 'Deleted'})
