from fastapi import APIRouter, HTTPException, status, Header
from typing import Optional
from pydantic import EmailStr, BaseModel
from app.config.config import settings
from app.schemas.user_schema import UserSchema, UserResponse, UserLogin, UserOut, NewPass, ForgetPass
from app.services.user_service import UserService
from app.utils.jwt import generate_token
from app.utils.bcrypt import verify_hash_pass, get_hash_pass
from app.utils.rand_str import rand_str
from app.utils.send_mail import send_mail

user_router = APIRouter()


@user_router.post("/register", summary="User Registration", response_model=UserResponse)
async def register_user(data: UserSchema):
    user = await UserService.create_user(data)
    token = generate_token(user.id)

    return {
        "message": "Registered Successfully",
        "user": user,
        "token": token
    }


@user_router.post("/oauth", summary="Authentication with Google/Facebook")
async def oauth(data: UserOut):
    user = await UserService.get_user_by_email(data.email)
    if not user:
        password = rand_str(N=12)
        hash_pass = get_hash_pass(password)
        user = await UserService.create_user({
            "firstName": data.firstName,
            "lastName": data.lastName,
            "email": data.email,
            "password": hash_pass
        })
        token = generate_token(user.id)
        return {
            "message": "Registered Successfully",
            "user": user,
            "token": token
        }

    token = generate_token(user.id)
    return {
        "message": "Logged In Successfully",
        "user": user,
        "token": token
    }


@user_router.post("/login", summary="User Login", response_model=Optional[UserResponse])
async def login_user(data: UserLogin):
    user = await UserService.get_user_by_email(data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Account Doesn't Exist"
            }
        )
    if not verify_hash_pass(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Incorrect Password"
            }
        )

    token = generate_token(user.id)

    return {
        "message": "Logged In Successfully",
        "user": user,
        "token": token
    }


@user_router.post("/newpass", summary="Create New Password")
async def login_user(data: NewPass, token: str | None = Header(default=None)):
    user = await UserService.authenticate(token)
    hash_pass = get_hash_pass(data.password)
    await UserService.update_user(str(user.id), {"password": hash_pass})
    return {"message": "password updated successfully"}


@user_router.post("/forgetpass", summary="Forget Password")
async def login_user(data: ForgetPass):
    user = await UserService.get_user_by_email(data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Account Doesn't Exist"
            }
        )
    password = rand_str(N=12)
    hash_pass = get_hash_pass(password)
    await UserService.update_user(str(user.id), {"password": hash_pass})
    send_mail(
        data.email,
        "Password Recovery",
        html=f"""\
            <html>
                <head></head>
                <body>
                    <p>your password has been set to {password}.</p>
                    <p>login <a href="{settings.PROJECT_URL}/login" target="_blank">here</a> and change the password</p>
                    <p>Thanks for using our service</p>
                </body>
            </html>
        """
    )
    return {"message": "Recovery Mail sent to your Email"}
