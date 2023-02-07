from flask import jsonify, request

from app.extensions import db
from app.models.product import Product
from app.product import bp
from app.product.serializers import (ProductCreationSerializer,
                                     ProductListItemSerializer,
                                     ProductSerializer)

product_serializer = ProductSerializer()
product_list_serializer = ProductListItemSerializer(many=True)
product_creation_serializer = ProductCreationSerializer()


@bp.route('/products', methods=['GET'])
def read_product_list():
    user_id = request.args.get('user_id')

    if user_id and not user_id.isnumeric():
        return jsonify({'message': 'Parameter "user_id" is invalid.'}), 400

    query = db.session.query(Product)

    if user_id:
        query = query.filter(Product.user_id == int(user_id))

    products = query.all()

    return product_list_serializer.dump(products)


@bp.route('/products/<int:id>', methods=['GET'])
def read_product_details(id):
    product = db.session.query(Product).get(id)

    if product is None:
        return jsonify({'message': 'Product not found.'}), 404

    return product_serializer.dump(product)


@bp.route('/products', methods=['POST'])
def create_product():
    user_id = 1  # TODO: auth

    error = product_creation_serializer.validate(request.json)

    if error:
        return jsonify(error), 422

    new_product = Product(name=request.json.get('name'),
                          description=request.json.get('description'),
                          image_url=request.json.get('image_url'),
                          price=request.json.get('price'),
                          user_id=user_id)

    db.session.add(new_product)
    db.session.commit()

    return product_serializer.dump(new_product)


@bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = db.session.query(Product).get(id)

    if product is None:
        return jsonify({'message': 'Product not found.'}), 404

    error = product_creation_serializer.validate(request.json)

    if error:
        return jsonify(error), 422

    product.name = request.json.get('name')
    product.description = request.json.get('description')
    product.image_url = request.json.get('image_url')
    product.price = request.json.get('price')

    db.session.commit()

    return product_serializer.dump(product)


@bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.query(Product).get(id)

    if product is None:
        return jsonify({'message': 'Product not found.'}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Deleted'})
