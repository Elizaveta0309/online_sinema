from datetime import datetime, timedelta, timezone

import jwt

from tests.settings import test_settings


def encode_user(user: dict) -> str:
    print(user)
    user['exp'] =  datetime.now(timezone.utc) + timedelta(10)
    return jwt.encode(
        user,
        test_settings.secret_key,
        algorithm='HS256',
    )
