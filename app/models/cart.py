from mongoengine import Document, fields
import datetime
from app.models.user import User
from app.models.product import Product


class CartItem(Document):
    user_id = fields.ReferenceField(User, required=True)
    product_id = fields.ReferenceField(Product, required=True)
    quantity = fields.IntField(default=1)  # Quantity of the product
    createdAt = fields.DateTimeField(default=datetime.datetime.utcnow)
    updatedAt = fields.DateTimeField(default=datetime.datetime.utcnow, auto_now=True)  

    meta = {
        'collection': 'cart_items'
    }
