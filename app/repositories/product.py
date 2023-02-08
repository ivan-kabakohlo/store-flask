from app.models.product import Product
from app.repositories.base import BaseRepository
from app.schemas.product import product_schema, products_schema


class ProductRepository(BaseRepository):
    def __init__(self, Model, schema, schema_many):
        super().__init__(Model, schema, schema_many)


product_repository = ProductRepository(Product, product_schema, products_schema)
