from app.extensions import db


class BaseRepository:
    def __init__(self, Model, schema, schema_many):
        self.Model = Model
        self.schema = schema
        self.schema_many = schema_many

    def read_all(self):
        entities = db.session.query(self.Model).all()
        return self.schema_many.dump(entities)

    def read_by_id(self, id):
        entity = db.session.query(self.Model).get_or_404(id)
        return self.schema.dump(entity)

    def create(self, body):
        deserialized = self.schema.load(body)
        new_entity = self.Model(**deserialized)

        db.session.add(new_entity)
        db.session.commit()

        return self.schema.dump(new_entity)

    def update_by_id(self, id, body):
        entity = db.session.query(self.Model).get_or_404(id)

        self.schema.load(body)

        for key, value in body.items():
            setattr(entity, key, value)

        db.session.commit()

        return self.schema.dump(entity)

    def delete_by_id(self, id):
        entity = db.session.query(self.Model).get_or_404(id)

        db.session.delete(entity)
        db.session.commit()
