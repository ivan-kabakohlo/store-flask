from marshmallow import fields, validate

from app.extensions import ma
from app.models.product import Product
from app.user.serializers import UserSerializer


class ProductSerializer(ma.Schema):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'image_url',
                  'price', 'created_at', 'updated_at', 'user')

    user = ma.Nested(UserSerializer)


class ProductListItemSerializer(ma.Schema):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'image_url',
                  'price', 'user_id', 'created_at', 'updated_at')


class ProductCreationSerializer(ma.Schema):
    name = fields.String(required=True, allow_none=False,
                         validate=validate.Length(min=4, max=60))
    description = fields.String(required=False,
                                validate=validate.Length(max=2000))
    image_url = fields.Url()
    price = fields.Float(required=True,
                         validate=validate.Range(0, 1_000_000_000))
