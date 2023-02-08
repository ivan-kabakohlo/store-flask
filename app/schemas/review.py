from marshmallow import fields, validate

from app.extensions import ma
from app.models.review import Review
from app.schemas.user import UserSchema


class ReviewSchema(ma.Schema):
    product_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    text = fields.String(required=True, allow_none=False,
                         validate=validate.Length(min=4, max=2000))

    class Meta:
        model = Review
        fields = ('id', 'text', 'product_id', 'user_id',
                  'created_at', 'updated_at', 'user')

    user = ma.Nested(UserSchema)


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
