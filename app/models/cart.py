from mongoengine import Document, fields
import datetime
from app.models.user import User

class CartItem(Document):
    user_id = fields.ReferenceField(User, required=True)
    product_id = fields.StringField(required=True)
    quantity = fields.IntField(default=1)  # Quantity of the product
    createdAt = fields.DateTimeField(default=datetime.datetime.utcnow)
    updatedAt = fields.DateTimeField(default=datetime.datetime.utcnow, auto_now=True)  

    meta = {
        'collection': 'cart_items'
    }
