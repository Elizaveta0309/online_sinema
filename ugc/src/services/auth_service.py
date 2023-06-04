import logging
from http import HTTPStatus

import jwt
from fastapi import HTTPException

from src.config import Settings

settings = Settings()
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


class Auth:
    secret = settings.jwt_key

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(
                token,
                'top_secret',
                algorithms='HS256',
                options={'verify_signature': False},
            )
            logging.info(payload)
            if payload['sub']:
                return payload['sub']
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Scope for the token is invalid',
            )
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='Token expired'
            ) from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token'
            ) from e
