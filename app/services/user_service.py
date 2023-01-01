from fastapi import HTTPException, status
from app.schemas.user_schema import UserSchema
from app.models.user_model import User
from app.utils.bcrypt import get_hash_pass
from pydantic import EmailStr
from bson.objectid import ObjectId
from typing import Optional
from app.utils.jwt import decode_token


class UserService:
    @staticmethod
    async def create_user(user: UserSchema):
        try:
            user_in = User(
                firstName=user.firstName,
                lastName=user.lastName,
                email=user.email,
                password=get_hash_pass(user.password)
            )
            user = await user_in.save()
            return user
        except Exception as error:
            return error

    @staticmethod
    async def update_user(id, data):
        try:
            user = await UserService.get_user_by_id(id)
            await user.update({"$set": data})
        except Exception as error:
            return error

    @staticmethod
    async def authenticate(token: str) -> Optional[User]:
        try:
            decoded = decode_token(token)
            if not decoded:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "message": "Not Authorized"
                    }
                )
            user = await UserService.get_user_by_id(decoded)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "message": "User Not Found"
                    }
                )
            return user
        except Exception as error:
            print("error in user_service authenticate method", error)
            return error

    @staticmethod
    async def get_user_by_email(email: EmailStr) -> Optional[User]:
        user = await User.find_one({"email": email})
        return user

    @staticmethod
    async def get_user_by_id(id: str) -> Optional[User]:
        user = await User.find_one({"_id": ObjectId(id)})
        return user
