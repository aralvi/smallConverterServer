from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    firstName: str = Field(..., description="first name")
    lastName: str = Field(..., description="last name")
    email: EmailStr = Field(..., description="UserEmail")
    password: str = Field(..., description="User Password")


class UserOut(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr


class UserResponse(BaseModel):
    message: str
    user: UserOut
    token: str


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="UserEmail")
    password: str = Field(..., description="User Password")


class NewPass(BaseModel):
    password: str


class ForgetPass(BaseModel):
    email: EmailStr
