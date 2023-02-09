from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.extensions import db


class Review(db.Model):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(2000))
    author_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author = relationship('User', back_populates='reviews')
    product = relationship('Product', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}>'
