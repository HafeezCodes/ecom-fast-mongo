# import jwt
# from datetime import datetime, timedelta
# from app.settings import settings
# from app.constants import constants

# def create_access_token(data: dict) -> str:
#     expires_delta = timedelta(days=constants.ACCESS_TOKEN_EXPIRE_DAYS)
#     expire = datetime.utcnow() + expires_delta
#     to_encode = data.copy()
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
#     return encoded_jwt

# def create_refresh_token(data: dict) -> str:
#     expires_delta = timedelta(days=constants.REFRESH_TOKEN_EXPIRE_DAYS)
#     expire = datetime.utcnow() + expires_delta
#     to_encode = data.copy()
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
#     return encoded_jwt

# def verify_token(token: str) -> dict:
#     try:
#         payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
#         return payload
#     except jwt.ExpiredSignatureError:
#         raise ValueError("Token has expired")
#     except jwt.InvalidTokenError:
#         raise ValueError("Invalid token")


import jwt
from datetime import datetime, timedelta
from app.settings import settings
from app.constants import constants

def create_access_token(data: dict) -> str:
    expires_delta = timedelta(days=constants.ACCESS_TOKEN_EXPIRE_DAYS)
    expire = datetime.utcnow() + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    expires_delta = timedelta(days=constants.REFRESH_TOKEN_EXPIRE_DAYS)
    expire = datetime.utcnow() + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        print(f"Token Payload: {payload}")  # Debug log
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


