from flask_sqlalchemy.model import Model
from marshmallow.schema import Schema

from app.models.product import Product
from app.repositories.base import BaseRepository
from app.schemas.product import product_schema, products_schema


class ProductRepository(BaseRepository):
    def __init__(self, Product: Model, product_schema: Schema, products_schema: Schema):
        super().__init__(Model=Product, schema=product_schema, schema_many=products_schema)


product_repository = ProductRepository(Product, product_schema, products_schema)
