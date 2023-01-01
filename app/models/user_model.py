from beanie import Document, Indexed
from pydantic import EmailStr
from typing import Optional


class User(Document):
    firstName: str
    lastName: str
    email: Indexed(EmailStr, unique=True)
    password: str
    disabled: Optional[bool] = False

    class Settings:
        name = "users"
