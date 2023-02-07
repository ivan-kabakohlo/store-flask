import os
from datetime import date

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, validate
from sqlalchemy import (Column, Date, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

app = Flask(__name__)

ma = Marshmallow(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(basedir, "store.db")

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(60), nullable=False, unique=True)
    email = Column(String(254), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    avatar_url = Column(String(2048))
    bio = Column(String(2000))
    birthday = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    products = relationship("Product", back_populates="user",
                            cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user",
                           cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'


class Product(db.Model):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    description = Column(String(2000))
    image_url = Column(String(2048))
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="products")
    reviews = relationship("Review", back_populates="product",
                           cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Product {self.id}>'


class Review(db.Model):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(2000))
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

    def __repr__(self):
        return f'<Review {self.id}>'


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ("id", "username", "email", "avatar_url",
                  "bio", "birthday", "created_at", "updated_at")


class ProductSchema(ma.Schema):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "image_url",
                  "price", "created_at", "updated_at", "user")

    user = ma.Nested(UserSchema)


class ProductListItemSchema(ma.Schema):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "image_url",
                  "price", "user_id", "created_at", "updated_at")


class ProductCreationSchema(ma.Schema):
    name = fields.String(required=True, allow_none=False,
                         validate=validate.Length(min=4, max=60))
    description = fields.String(required=False,
                                validate=validate.Length(max=2000))
    image_url = fields.Url()
    price = fields.Float(required=True,
                         validate=validate.Range(0, 1_000_000_000))


class ReviewSchema(ma.Schema):
    class Meta:
        model = Review
        fields = ("id", "text", "product_id",
                  "created_at", "updated_at", "user")

    user = ma.Nested(UserSchema)


class ReviewCreationSchema(ma.Schema):
    product_id = fields.Integer()
    text = fields.String(required=True, allow_none=False,
                         validate=validate.Length(min=4, max=2000))


product_schema = ProductSchema()

product_list_item_schema = ProductListItemSchema(many=True)

product_creation_schema = ProductCreationSchema()

review_schema = ReviewSchema()

review_list_item_schema = ReviewSchema(many=True)

review_creation_schema = ReviewCreationSchema()


@app.route("/products", methods=["GET"])
def read_product_list():
    user_id = request.args.get("user_id")

    if user_id and not user_id.isnumeric():
        return "Parameter \"user_id\" is invalid.", 400

    query = db.session.query(Product)

    if user_id:
        query = query.filter(Product.user_id == int(user_id))

    products = query.all()

    return product_list_item_schema.dump(products)


@app.route("/products/<int:id>", methods=["GET"])
def read_product_details(id):
    product = db.session.query(Product).get(id)

    if (product is None):
        return jsonify({"message": "Product not found."}), 404

    return product_schema.dump(product)


@app.route("/products", methods=["POST"])
def create_product():
    user_id = 1  # TODO: auth

    error = product_creation_schema.validate(request.json)

    if error:
        return jsonify(error), 422

    new_product = Product(name=request.json.get("name"),
                          description=request.json.get("description"),
                          image_url=request.json.get("image_url"),
                          price=request.json.get("price"),
                          user_id=user_id)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.dump(new_product)


@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = db.session.query(Product).filter_by(id=id).first()

    if product is None:
        return jsonify({"message": "Product not found."}), 404

    error = product_creation_schema.validate(request.json)

    if error:
        return jsonify(error), 422

    product.name = request.json.get("name")
    product.description = request.json.get("description")
    product.image_url = request.json.get("image_url")
    product.price = request.json.get("price")

    db.session.commit()

    return product_schema.dump(product)


@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = db.session.query(Product).filter_by(id=id).first()

    if product is None:
        return jsonify({"message": "Product not found."}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Deleted"})


@app.route("/reviews", methods=["GET"])
def read_reviews():
    product_id = request.args.get("product_id")
    user_id = request.args.get("user_id")

    errors = list()

    if product_id and not product_id.isnumeric():
        errors.append("Parameter \"product_id\" is invalid.")

    if user_id and not user_id.isnumeric():
        errors.append("Parameter \"user_id\" is invalid.")

    if errors != []:
        return jsonify(errors), 400

    query = db.session.query(Review)

    if product_id:
        query = query.filter(Review.product_id == int(product_id))

    if user_id:
        query = query.filter(Review.user_id == int(user_id))

    reviews = query.all()

    return review_list_item_schema.dump(reviews)


@app.route("/reviews/<int:id>", methods=["GET"])
def read_review(id):
    review = db.session.query(Review).get(id)

    if (review is None):
        return jsonify({"message": "Review not found."}), 404

    return review_schema.dump(review)


@app.route("/reviews", methods=["POST"])
def create_review():
    user_id = 1  # TODO: auth

    text = request.json.get("text")
    product_id = request.json.get("product_id")

    product = db.session.query(Product).filter_by(id=product_id).first()

    if product is None:
        return jsonify({"message": "Product not found."}), 404

    error = review_creation_schema.validate(request.json)

    if error:
        return jsonify(error), 422

    new_review = Review(text=text, product_id=product_id, user_id=user_id)

    db.session.add(new_review)
    db.session.commit()

    return review_schema.dump(new_review)


@app.route("/reviews/<int:id>", methods=["PUT"])
def update_review(id):
    user_id = 1  # TODO: auth

    text = request.json.get("text")
    product_id = request.json.get("product_id")

    review = db.session.query(Review).filter_by(id=id).first()

    if review is None:
        return jsonify({"message": "Review not found."}), 404

    if review.product_id != product_id:
        return jsonify({"message": "Field \"product_id\" cannot be changed."}), 400

    if review.user_id != user_id:
        return jsonify({"message": "Review can be changed only by its author."}), 403

    error = review_creation_schema.validate(request.json)

    if error:
        return jsonify(error), 422

    review.text = text

    db.session.commit()

    return review_schema.dump(review)


@app.route("/reviews/<int:id>", methods=["DELETE"])
def delete_review(id):
    user_id = 1  # TODO: auth

    review = db.session.query(Review).filter_by(id=id).first()

    if review is None:
        return jsonify({"message": "Review not found."}), 404

    if review.user_id != user_id:
        return jsonify({"message": "Review can be deleted only by its author."}), 403

    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Deleted"})


@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Database has been created!")


@app.cli.command("db_seed")
def db_seed():
    review_1 = Review(
        text="Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?")
    review_2 = Review(
        text="Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur")
    review_3 = Review(
        text="Vel illum qui dolorem eum fugiat quo voluptas nulla pariatur")

    product_1 = Product(
        name="Product 1",
        description="Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
        image_url=None,
        price=199.99,
        reviews=[review_1, review_2])
    product_2 = Product(
        name="Product 2",
        description="Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        image_url=None,
        price=999.99,
        reviews=[review_3])

    user_1 = User(
        username="admin", email="testmail1@mail.com",
        password="test123!", avatar_url=None,
        bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        birthday=date(2002, 6, 22), products=[product_1],
        reviews=[review_2, review_3])
    user_2 = User(
        username="ivan",
        email="testmail2@mail.com",
        password="test123!",
        avatar_url=None,
        bio="Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        birthday=None,
        products=[product_2],
        reviews=[review_1])

    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()

    print("Database has been seeded!")


@app.cli.command("db_drop")
def db_drop_all():
    db.drop_all()
    print("Database has been dropped!")


if __name__ == "__app__":
    app.run()
