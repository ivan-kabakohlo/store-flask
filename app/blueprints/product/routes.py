from flask import jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from app.blueprints.product import bp
from app.blueprints.product.controller import ProductController

product_controller = ProductController()


@bp.route('/products', methods=['GET'])
def read_products():
    return product_controller.read_products()


@bp.route('/products/<int:id>', methods=['GET'])
def read_product(id: int):
    try:
        return product_controller.read_product(id)
    except NoResultFound as e:
        return jsonify(e.args[0]), 404


@bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    try:
        return product_controller.create_product(request.json)
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id: int):
    try:
        return product_controller.update_product(id, request.json)
    except NoResultFound as e:
        return jsonify(e.args[0]), 404
    except ValidationError as e:
        return jsonify(e.normalized_messages()), 422


@bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id: int):
    try:
        result = product_controller.delete_product(id)
        return jsonify(result)
    except NoResultFound as e:
        return jsonify(e.args[0]), 404
