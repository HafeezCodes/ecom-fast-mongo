from mongoengine import Document, fields
import datetime
from passlib.context import CryptContext
from pydantic import EmailStr
from mongoengine.errors import DoesNotExist



class User(Document):
    name = fields.StringField(max_length=100, required=True)
    email = fields.EmailField(unique=True, required=True)
    password = fields.StringField(required=True)
    dob = fields.DateField(required=True)
    createdAt = fields.DateTimeField(default=datetime.datetime.utcnow)
    updatedAt = fields.DateTimeField(default=datetime.datetime.utcnow, auto_now=True)  


    meta = {
        'collection': 'users'
    }

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def check_user_exists(email: EmailStr) -> bool:
    return User.objects(email=email).first() is not None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(email: EmailStr):
    try:
        return User.objects.get(email=email)
    except DoesNotExist:
        return None

