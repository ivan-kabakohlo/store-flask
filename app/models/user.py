from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(60), nullable=False, unique=True)
    email = Column(String(254), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    avatar_url = Column(String(2048))
    bio = Column(String(2000))
    birthday = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    products = relationship('Product', back_populates='user',
                            cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='user',
                           cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'
