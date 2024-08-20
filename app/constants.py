from dataclasses import dataclass
from app.settings import settings

@dataclass(frozen=True)
class Constants:
    ALLOWED_HOSTS = '*'
    DEBUG = True
    ACCESS_TOKEN_EXPIRE_DAYS = 1
    REFRESH_TOKEN_EXPIRE_DAYS = 30
    MONGODB_URI = settings.MONGODB_URI

constants = Constants()
