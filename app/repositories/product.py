from flask_sqlalchemy.model import Model
from marshmallow.schema import Schema

from app.models.product import Product
from app.repositories.base import BaseRepository
from app.schemas.product import ProductSchema


class ProductRepository(BaseRepository):
    def __init__(self, Product: Model, ProductSchema: Schema):
        super().__init__(Product, ProductSchema)


product_repository = ProductRepository(Product, ProductSchema)
