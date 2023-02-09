from marshmallow import fields, validate

from app.extensions import ma
from app.models.product import Product
from app.schemas.user import UserSchema


class ProductSchema(ma.Schema):
    name = fields.String(required=True,
                         validate=validate.Length(min=4, max=60))
    description = fields.String(required=False,
                                validate=validate.Length(max=2000))
    image_url = fields.Url(required=False)
    price = fields.Float(required=True,
                         validate=validate.Range(0, 1_000_000_000))
    seller_id = fields.Integer(required=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'image_url', 'price',
                  'created_at', 'updated_at', 'seller_id', 'seller')

    seller = ma.Nested(UserSchema)


class ProductsSchema(ProductSchema):
    class Meta(ProductSchema.Meta):
        exclude = ['seller']


product_schema = ProductSchema()
products_schema = ProductsSchema(many=True)
