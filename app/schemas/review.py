from marshmallow import fields, validate

from app.extensions import ma
from app.models.review import Review


class ReviewSchema(ma.Schema):
    product_id = fields.Integer(required=True)
    author_id = fields.Integer(required=True)
    text = fields.String(required=True, allow_none=False,
                         validate=validate.Length(min=4, max=2000))

    class Meta:
        model = Review
        fields = ('id', 'text', 'author_id', 'product_id',
                  'created_at', 'updated_at')
