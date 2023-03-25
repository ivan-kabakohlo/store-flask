from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from app.blueprints.product import bp
from app.blueprints.product.controller import ProductController

product_controller = ProductController()


@bp.route('/products', methods=['GET'])
def read_product_list():
    return product_controller.read_product_list()


@bp.route('/products/<int:id>', methods=['GET'])
def read_product(id: int):
    try:
        return product_controller.read_product(id=id)
    except NoResultFound:
        return jsonify({'message': 'Product not found'}), 404


@bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    user = get_jwt_identity()

    try:
        return product_controller.create_product(
            user_id=user['id'], body=request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id: int):
    user = get_jwt_identity()

    try:
        return product_controller.update_product(
            id=id, user_id=user['id'], body=request.json)
    except NoResultFound:
        return jsonify({'message': 'Product not found'}), 404
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id: int):
    user = get_jwt_identity()

    try:
        result = product_controller.delete_product(id=id, user_id=user['id'])
        return jsonify(result)
    except NoResultFound:
        return jsonify({'message': 'Product not found'}), 404
