import jwt
from aiohttp import ClientSession
from jwt import InvalidSignatureError, ExpiredSignatureError

from src.core.config import settings


def get_items_source(data):
    return list(map(lambda x: x['_source'], data['hits']['hits']))


def build_cache_key(f, args, obj) -> str:
    query = obj if isinstance(obj, str) else ':'.join(map(str, obj.__dict__.values()))
    return (
            f.__name__
            + ':'
            + str(args.index)
            + ':'
            + query
    )


def jwt_decode(token):
    return jwt.decode(token, settings.SECRET, algorithms='HS256')


def verify_auth(request):
    token_encoded = request.cookies.get('token')
    refresh_encoded = request.cookies.get('refresh')
    token = jwt_decode(token_encoded)
    refresh = jwt_decode(refresh_encoded)
    return token, refresh


def is_token_expired(token):
    try:
        jwt.decode(token, settings.SECRET, algorithms='HS256')
        return False
    except ExpiredSignatureError:
        return True


def is_token_valid(token):
    try:
        jwt.decode(token, settings.SECRET, algorithms='HS256')
        return True
    except InvalidSignatureError:
        return False
    except ExpiredSignatureError:
        return True


async def generate_new_tokens(token):
    url = f'{settings.AUTH_API_URL}/refresh'
    async with ClientSession() as session:
        async with session.post(url, json={'refresh': token}) as response:
            return await response.json()
