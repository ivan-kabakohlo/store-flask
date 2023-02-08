from app.extensions import db
from app.models.review import Review
from app.repositories.base import BaseRepository
from app.schemas.review import review_schema, reviews_schema


class ReviewRepository(BaseRepository):
    def __init__(self, Review, review_schema, reviews_schema):
        super().__init__(Model=Review, schema=review_schema, schema_many=reviews_schema)
        self.Review = Review
        self.reviews_schema = reviews_schema

    def read_all(self, product_id, user_id):
        if not product_id and not user_id:
            return super().read_all()

        query = db.session.query(self.Model)

        if product_id:
            query = query.filter(self.Review.product_id == product_id)
        if user_id:
            query = query.filter(self.Review.user_id == user_id)

        reviews = query.all()

        return self.reviews_schema.dump(reviews)


review_repository = ReviewRepository(Review, review_schema, reviews_schema)
