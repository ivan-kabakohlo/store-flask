from marshmallow import fields, validate

from app.extensions import ma
from app.models.review import Review
from app.user.serializers import UserSerializer


class ReviewSerializer(ma.Schema):
    class Meta:
        model = Review
        fields = ('id', 'text', 'product_id',
                  'created_at', 'updated_at', 'user')

    user = ma.Nested(UserSerializer)


class ReviewCreationSerializer(ma.Schema):
    product_id = fields.Integer()
    text = fields.String(required=True, allow_none=False,
                         validate=validate.Length(min=4, max=2000))
