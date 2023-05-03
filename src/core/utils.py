import jwt
from jwt import ExpiredSignatureError

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


def is_token_expired(token):
    try:
        jwt.decode(token, settings.SECRET, algorithms='HS256')
        return False
    except ExpiredSignatureError:
        return True
