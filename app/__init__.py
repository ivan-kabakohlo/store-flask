from flask import Flask

from app.extensions import db, ma
from app.seed import seed
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    from app.product import bp as product_bp
    from app.review import bp as review_bp
    from app.user import bp as user_bp

    app.register_blueprint(product_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(user_bp)

    @app.cli.command('db_create')
    def db_create():
        db.create_all()
        print('Database has been created.')

    @app.cli.command('db_seed')
    def db_seed():
        seed()
        print('Database has been seeded.')

    @app.cli.command('db_drop')
    def db_drop_all():
        db.drop_all()
        print('Database has been dropped.')

    return app
