from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from starlette import status


def valid_user(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        user = authorize.get_raw_jwt()
        user["id"] = authorize.get_jwt_subject()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided"
        )
    return user