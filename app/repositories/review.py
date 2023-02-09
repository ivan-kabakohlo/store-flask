from flask_sqlalchemy.model import Model
from marshmallow.schema import Schema

from app.extensions import db
from app.models.review import Review
from app.repositories.base import BaseRepository
from app.schemas.review import review_schema, reviews_schema


class ReviewRepository(BaseRepository):
    def __init__(self, Review: Model, review_schema: Schema, reviews_schema: Schema):
        super().__init__(Model=Review, schema=review_schema, schema_many=reviews_schema)
        self.Review = Review
        self.reviews_schema = reviews_schema

    def read_all(self, product_id: int, author_id: int):
        if not product_id and not author_id:
            return super().read_all()

        query = db.session.query(self.Model)

        if product_id:
            query = query.filter(self.Review.product_id == product_id)
        if author_id:
            query = query.filter(self.Review.author_id == author_id)

        reviews = query.all()

        return self.reviews_schema.dump(reviews)


review_repository = ReviewRepository(Review, review_schema, reviews_schema)
