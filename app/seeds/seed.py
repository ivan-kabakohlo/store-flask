from datetime import date

from app.extensions import db
from app.models.product import Product
from app.models.review import Review
from app.models.user import User


def seed():
    review_1 = Review(
        text='Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?')
    review_2 = Review(
        text='Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur')
    review_3 = Review(
        text='Vel illum qui dolorem eum fugiat quo voluptas nulla pariatur')

    product_1 = Product(
        name='Product 1',
        description='Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur',
        image_url=None,
        price=199.99,
        reviews=[review_1, review_2])
    product_2 = Product(
        name='Product 2',
        description='Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image_url=None,
        price=999.99,
        reviews=[review_3])

    user_1 = User(
        username='admin',
        email='testmail1@mail.com',
        password='test123!',
        avatar_url=None,
        bio='Lorem ipsum dolor sit amet, consectetur adipiscing elit',
        birthday=date(2002, 6, 22),
        products=[product_1],
        reviews=[review_2, review_3])
    user_2 = User(
        username='ivan',
        email='testmail2@mail.com',
        password='test123!',
        avatar_url=None,
        bio='Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
        birthday=None,
        products=[product_2],
        reviews=[review_1])

    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()
