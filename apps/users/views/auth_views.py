import logging

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from fastapi_jwt_auth import AuthJWT
from apps.users.functions import verify_password
from apps.users.models import User
from apps.users.schemas import CreateUser, UserSchema, GetAuthSchema, LoginSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

logger = logging.getLogger(__name__)


@auth_router.post("/sign-up/", status_code=status.HTTP_201_CREATED, response_model=GetAuthSchema)
async def create_user(
        user: CreateUser,
        authorize: AuthJWT = Depends()
):
    if await User.get_or_none(username=user.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with {user.username} already exists"
        )
    await User.check_mobile_exist(mobile=user.mobile)
    logger.debug(f"Trying to create user with data: '{user}'")
    user_response = await User.create_user(user.dict(exclude_unset=True))
    is_password_verified = verify_password(
        plain_password=user.password_hash,
        hashed_password=user_response.password_hash
    )
    payload = {
        "id": user_response.id,
        "username": user.username
    }
    if is_password_verified:
        response = {
            "access": authorize.create_access_token(
                subject=str(user_response.id), user_claims=payload, fresh=True
            ),
            "refresh": authorize.create_refresh_token(
                subject=str(user_response.id),
                user_claims=payload
            ),
            "user": user_response,
        }
        return response


@auth_router.post("/login/", response_model=GetAuthSchema)
async def login(user: LoginSchema, authorize: AuthJWT = Depends()):
    user_instance = await User.get_user_by_username(username=user.username)
    is_password_verified = verify_password(
        plain_password=user.password_hash,
        hashed_password=user_instance.password_hash
    )
    payload = {
        "id": user_instance.id,
        "username": user.username,
        "is_active": user_instance.is_active,
        "is_superuser": user_instance.is_superuser
    }
    if is_password_verified:
        response = {
            "access": authorize.create_access_token(
                subject=str(user_instance.id), user_claims=payload, fresh=True
            ),
            "refresh": authorize.create_refresh_token(
                subject=str(user_instance.id),
                user_claims=payload
            ),
            "user": user_instance,
        }
        return response
    else:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"username and password are incorrect"
        )





