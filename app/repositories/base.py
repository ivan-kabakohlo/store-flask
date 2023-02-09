from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model

from app.extensions import db


class BaseRepository:
    def __init__(self, Model: Model, Schema: Schema):
        self.Model = Model
        self.schema = Schema()
        self.schema_many = Schema(many=True)

    def read_all(self):
        entities = db.session.query(self.Model).all()
        return self.schema_many.dump(entities)

    def read_by_id(self, id: int):
        entity = db.session.query(self.Model).get_or_404(id)
        return self.schema.dump(entity)

    def create(self, body: dict = {}):
        deserialized = self.schema.load(body)
        new_entity = self.Model(**deserialized)

        db.session.add(new_entity)
        db.session.commit()

        return self.schema.dump(new_entity)

    def update_by_id(self, id: int, body: dict = {}):
        entity = db.session.query(self.Model).get_or_404(id)

        self.schema.load(body)

        for key, value in body.items():
            setattr(entity, key, value)

        db.session.commit()

        return self.schema.dump(entity)

    def delete_by_id(self, id: int):
        entity = db.session.query(self.Model).get_or_404(id)

        db.session.delete(entity)
        db.session.commit()
