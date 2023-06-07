from functools import wraps
from http import HTTPStatus

from fastapi import HTTPException
from jose import ExpiredSignatureError, jwt

from src.config import settings


def check_permission(required_role: list):
    def wrapper(func):
        @wraps(func)
        async def decorator(*args, **kwargs):
            # request = kwargs['request']
            # token = request.cookies.get('token')
            token = kwargs.get('request').credentials#
            try:
                decoded = jwt.decode(
                    token, settings.jwt_key, algorithms="HS256"
                )
            except ExpiredSignatureError as exp:
                return exp
            check_user_role(decoded['role'], required_role)
            kwargs['request'] = decoded
            response = await func(*args, **kwargs)
            return response

        return decorator

    return wrapper


def check_user_role(user_role: str, required_role: list):
    if user_role not in required_role:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Access denied'
        )
