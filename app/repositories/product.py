from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import and_

from app.extensions import db
from app.models.product import Product as ProductModel
from app.repositories.base import BaseRepository
from app.schemas.product import ProductSchema


class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(Model=ProductModel, Schema=ProductSchema)

        self.Product = ProductModel
        self.product_schema = ProductSchema()
        self.product_schema_update = ProductSchema(
            exclude=['seller_id'],
            partial=('name', 'description', 'image_url', 'price'))

    def create(self, seller_id, body: dict):
        return super().create(body={**body, 'seller_id': seller_id})

    def update_by_id(self, id: int, seller_id: int, body: dict):
        condition = and_(self.Product.id == id,
                         self.Product.seller_id == seller_id)
        product = db.session.query(self.Product).filter(condition).first()

        if product is None:
            raise NoResultFound({'message': 'Can not access this product.'})

        self.product_schema_update.load(body)

        for key, value in body.items():
            setattr(product, key, value)

        db.session.commit()

        return self.product_schema.dump(product)

    def delete_by_id(self, id: int, seller_id: int):
        condition = and_(self.Product.id == id,
                         self.Product.seller_id == seller_id)
        product = db.session.query(self.Product).filter(condition).first()

        if product is None:
            raise NoResultFound({'message': 'Can not access this product.'})

        db.session.delete(product)
        db.session.commit()
