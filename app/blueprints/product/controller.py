from app.repositories.product import ProductRepository


class ProductController:
    product_repository = ProductRepository()

    def read_products(self):
        return self.product_repository.read_all()

    def read_product(self, id: int):
        return self.product_repository.read_by_id(id)

    def create_product(self, body):
        return self.product_repository.create(body)

    def update_product(self, id: int, body):
        return self.product_repository.update_by_id(id, body)

    def delete_product(self, id: int):
        self.product_repository.delete_by_id(id)
        return {'message': 'Deleted'}
