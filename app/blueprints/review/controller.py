from app.repositories.review import ReviewRepository


class ReviewController:
    review_repository = ReviewRepository()

    def read_review_list(self, filters: dict = {}):
        product_id = filters.get('product_id', '')
        author_id = filters.get('author_id', '')

        product_id = int(product_id) if product_id.isdigit() else None
        author_id = int(author_id) if author_id.isdigit() else None

        return self.review_repository.read_all(
            product_id=product_id, author_id=author_id)

    def read_review(self, id: int):
        return self.review_repository.read_by_id(id=id)

    def create_review(self, user_id: int, body: dict):
        return self.review_repository.create(author_id=user_id, body=body)

    def update_review(self, id: int, user_id: int, body: dict):
        return self.review_repository.update_by_id(
            id=id, author_id=user_id, body=body)

    def delete_review(self, id: int, user_id: int):
        self.review_repository.delete_by_id(id=id, author_id=user_id)
        return {'message': 'Deleted'}
