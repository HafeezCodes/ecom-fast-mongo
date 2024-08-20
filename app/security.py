# from fastapi import HTTPException
# from mongoengine import DoesNotExist
# from fastapi.security import OAuth2PasswordBearer
# from app.utils.jwt import verify_token
# from app.models.user import User
# from datetime import datetime, timezone

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

# class UserAuthenticator:
#     def __init__(self):
#         pass

#     def check_user_existence(self, user_id: str) -> User:
#         try:
#             user = User.objects.get(id=user_id)
#         except DoesNotExist:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user

#     def verify_token(self, token: str) -> dict:
#         try:
#             payload = verify_token(token)
#             expiry = payload.get("exp")
#             if expiry and datetime.fromtimestamp(expiry, tz=timezone.utc) < datetime.now(timezone.utc):
#                 raise HTTPException(status_code=401, detail="Token has expired")
#             return payload
#         except ValueError as e:
#             raise HTTPException(status_code=401, detail=str(e))

#     def get_user_from_token(self, token: str) -> User:
#         payload = self.verify_token(token)
#         user_id_from_token = payload.get("sub")  # 'sub' is usually used for subject in JWT
        
#         if user_id_from_token is None:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         user = self.check_user_existence(user_id_from_token)
#         return user

#     def check_user_id_match(self, user_id_from_token: str, user_id: str):
#         if user_id_from_token != user_id:
#             raise HTTPException(status_code=403, detail="Not Authorized")

#     def authenticate_user(self, token: str, user_id: str) -> User:
#         current_user = self.get_user_from_token(token)
#         self.check_user_id_match(current_user.id, user_id)
#         return current_user


from bson import ObjectId
from fastapi import HTTPException
from mongoengine import DoesNotExist
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import verify_token
from app.models.user import User
from datetime import datetime, timezone

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

class UserAuthenticator:
    def __init__(self):
        pass

    def check_user_existence(self, user_id: str) -> User:
        try:
            user = User.objects.get(id=ObjectId(user_id))  # Convert string to ObjectId
            return user
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")

    def verify_token(self, token: str) -> dict:
        try:
            payload = verify_token(token)
            print(f"Decoded Token Payload: {payload}")  # Debug print
            expiry = payload.get("exp")
            if expiry and datetime.fromtimestamp(expiry, tz=timezone.utc) < datetime.now(timezone.utc):
                raise HTTPException(status_code=401, detail="Token has expired")
            return payload
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

    def get_user_from_token(self, token: str) -> User:
        payload = self.verify_token(token)
        user_id_from_token = payload.get("sub")  # 'sub' is usually used for subject in JWT
        
        if user_id_from_token is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = self.check_user_existence(user_id_from_token)
        return user

    def check_user_id_match(self, user_id_from_token: str, user_id: str):
        print(f"Comparing Token User ID: {user_id_from_token} with API User ID: {user_id}")  # Debug print
        if user_id_from_token != user_id:
            raise HTTPException(status_code=403, detail="Not Authorized")

    def authenticate_user(self, token: str, user_id: str) -> User:
        current_user = self.get_user_from_token(token)
        self.check_user_id_match(str(current_user.id), user_id)  # Convert ObjectId to string for comparison
        return current_user
