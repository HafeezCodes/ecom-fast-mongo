from mongoengine import Document, fields
import datetime

class Product(Document):
    name = fields.StringField(max_length=255, required=True)
    description = fields.StringField()
    price = fields.FloatField(required=True)
    stock = fields.IntField(required=True)
    createdAt = fields.DateTimeField(default=datetime.datetime.utcnow)
    updatedAt = fields.DateTimeField(auto_now=True)

    meta = {
        'collection': 'products'
    }

    def save(self, *args, **kwargs):
        self.updatedAt = datetime.datetime.utcnow()  # Update `updatedAt` before saving
        return super(Product, self).save(*args, **kwargs)