from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.extensions import db


class Product(db.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    description = Column(String(2000))
    image_url = Column(String(2048))
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('User', back_populates='products')
    reviews = relationship('Review', back_populates='product',
                           cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Product {self.id}>'
