from app.models.product import Product
from app.repositories.base import BaseRepository
from app.schemas.product import ProductSchema


class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(Model=Product, Schema=ProductSchema)
