import jwt
#from tests.settings import test_settings
from datetime import datetime, timezone, timedelta

def encode_user(user: dict) -> str:
    print(user)
    user['exp'] =  datetime.now(timezone.utc) + timedelta(10)
    payload = jwt.encode(
                user,
                'top_secret',
                algorithm='HS256',
            )
    return payload

a = {
    'role': 'admin',
    'user_id': 1
}

print(encode_user(a))