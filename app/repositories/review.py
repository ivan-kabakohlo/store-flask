from app.models.review import Review
from app.repositories.base import BaseRepository
from app.schemas.review import review_schema, reviews_schema


class ReviewRepository(BaseRepository):
    def __init__(self, Model, schema, schema_many):
        super().__init__(Model, schema, schema_many)


review_repository = ReviewRepository(Review, review_schema, reviews_schema)
