from flask import jsonify, request

from app.extensions import db
from app.models.product import Product
from app.models.review import Review
from app.review import bp
from app.review.serializers import ReviewCreationSerializer, ReviewSerializer

review_list_serializer = ReviewSerializer(many=True)
review_serializer = ReviewSerializer()
review_creation_serializer = ReviewCreationSerializer()


@bp.route('/reviews', methods=['GET'])
def read_reviews():
    product_id = request.args.get('product_id')
    user_id = request.args.get('user_id')

    errors = list()

    if product_id and not product_id.isnumeric():
        errors.append('Parameter "product_id" is invalid.')

    if user_id and not user_id.isnumeric():
        errors.append('Parameter "user_id" is invalid.')

    if errors != []:
        return jsonify(errors), 400

    query = db.session.query(Review)

    if product_id:
        query = query.filter(Review.product_id == int(product_id))

    if user_id:
        query = query.filter(Review.user_id == int(user_id))

    reviews = query.all()

    return review_list_serializer.dump(reviews)


@bp.route('/reviews/<int:id>', methods=['GET'])
def read_review(id):
    review = db.session.query(Review).get(id)

    if review is None:
        return jsonify({'message': 'Review not found.'}), 404

    return review_serializer.dump(review)


@bp.route('/reviews', methods=['POST'])
def create_review():
    user_id = 1  # TODO: auth

    text = request.json.get('text')
    product_id = request.json.get('product_id')

    product = db.session.query(Product).get(product_id)

    if product is None:
        return jsonify({'message': 'Product not found.'}), 404

    error = review_creation_serializer.validate(request.json)

    if error:
        return jsonify(error), 422

    new_review = Review(text=text, product_id=product_id, user_id=user_id)

    db.session.add(new_review)
    db.session.commit()

    return review_serializer.dump(new_review)


@bp.route('/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    user_id = 1  # TODO: auth

    text = request.json.get('text')
    product_id = request.json.get('product_id')

    review = db.session.query(Review).get(id)

    if review is None:
        return jsonify({'message': 'Review not found.'}), 404

    if review.product_id != product_id:
        return jsonify({'message': 'Field "product_id" cannot be changed.'}), 400

    if review.user_id != user_id:
        return jsonify({'message': 'Review can be changed only by its author.'}), 403

    error = review_creation_serializer.validate(request.json)

    if error:
        return jsonify(error), 422

    review.text = text

    db.session.commit()

    return review_serializer.dump(review)


@bp.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    user_id = 1  # TODO: auth

    review = db.session.query(Review).get(id)

    if review is None:
        return jsonify({'message': 'Review not found.'}), 404

    if review.user_id != user_id:
        return jsonify({'message': 'Review can be deleted only by its author.'}), 403

    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Deleted'})
