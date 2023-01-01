from typing import Union, Any
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.config.config import settings
from jose import jwt

def generate_token(subject: Union[dict, Any], expires_delta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRES_IN_MINUTES)
    
    to_encode = {"exp":expires_delta, "sub":str(subject)}
    jwt_encoded = jwt.encode(to_encode, settings.JWT_SECRET, "HS256")
    return jwt_encoded


def decode_token(token: str) -> Union[str, None]:
    decoded = jwt.decode(token, settings.JWT_SECRET)
    if decoded is None:
        return None
    else:
        return decoded["sub"]
