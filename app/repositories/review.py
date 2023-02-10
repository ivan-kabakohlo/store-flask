from app.extensions import db
from app.models.review import Review
from app.repositories.base import BaseRepository
from app.schemas.review import ReviewSchema


class ReviewRepository(BaseRepository):
    def __init__(self):
        super().__init__(Model=Review, Schema=ReviewSchema)
        self.Review = Review
        self.schema = ReviewSchema()

    def read_all(self, product_id: int, author_id: int):
        if not product_id and not author_id:
            return super().read_all()

        query = db.session.query(self.Model)

        if product_id:
            query = query.filter(self.Review.product_id == product_id)
        if author_id:
            query = query.filter(self.Review.author_id == author_id)

        reviews = query.all()

        return self.schema_many.dump(reviews, many=True)
