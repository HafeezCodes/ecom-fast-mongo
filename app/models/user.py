from mongoengine import Document, fields
import datetime

class User(Document):
    name = fields.StringField(max_length=100, required=True)
    email = fields.EmailField(unique=True, required=True)
    password = fields.StringField(required=True)
    dob = fields.DateField(required=True)
    createdAt = fields.DateTimeField(default=datetime.datetime.utcnow)
    updatedAt = fields.DateTimeField(auto_now=True)

    meta = {
        'collection': 'users'
    }
