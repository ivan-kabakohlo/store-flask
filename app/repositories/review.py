from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import and_

from app.extensions import db
from app.models.review import Review as ReviewModel
from app.repositories.base import BaseRepository
from app.schemas.review import ReviewSchema


class ReviewRepository(BaseRepository):
    def __init__(self):
        super().__init__(Model=ReviewModel, Schema=ReviewSchema)

        self.Review = ReviewModel
        self.review_schema = ReviewSchema()
        self.review_schema_update = ReviewSchema(
            exclude=['author_id', 'product_id'])

    def read_all(self, product_id: int, author_id: int):
        if not product_id and not author_id:
            return super().read_all()

        query = db.session.query(self.Model)

        if product_id:
            query = query.filter(self.Review.product_id == product_id)
        if author_id:
            query = query.filter(self.Review.author_id == author_id)

        reviews = query.all()

        return self.review_schema.dump(reviews, many=True)

    def create(self, author_id: int, body: dict = {}):
        return super().create(body={**body, 'author_id': author_id})

    def update_by_id(self, id: int, author_id: int, body: dict = {}):
        condition = and_(self.Review.id == id,
                         self.Review.author_id == author_id)
        review = db.session.query(self.Review).filter(condition).first()

        if review is None:
            raise NoResultFound({'message': 'Can not access this review.'})

        self.review_schema_update.load(body)

        for key, value in body.items():
            setattr(review, key, value)

        db.session.commit()

        return self.review_schema.dump(review)

    def delete_by_id(self, id: int, author_id: int):
        condition = and_(self.Review.id == id,
                         self.Review.author_id == author_id)
        review = db.session.query(self.Review).filter(condition).first()

        if review is None:
            raise NoResultFound({'message': 'Can not access this review.'})

        db.session.delete(review)
        db.session.commit()
