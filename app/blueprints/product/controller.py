from app.repositories.product import ProductRepository


class ProductController:
    product_repository = ProductRepository()

    def read_products(self):
        return self.product_repository.read_all()

    def read_product(self, id: int):
        return self.product_repository.read_by_id(id)

    def create_product(self, user_id: int, body):
        return self.product_repository.create(user_id, body)

    def update_product(self, id: int, user_id: int, body):
        return self.product_repository.update_by_id(id, user_id, body)

    def delete_product(self, id: int, user_id: int):
        self.product_repository.delete_by_id(id, user_id)
        return {'message': 'Deleted'}