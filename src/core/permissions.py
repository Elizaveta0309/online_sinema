from functools import wraps

from fastapi import HTTPException, status

from src.api.v1.models.film import Film
from src.core.utils import is_token_expired, jwt_decode


def premium_needed(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs['request']
        token = request.cookies.get('token')
        obj = await func(*args, **kwargs)

        error = validate_sub_query(obj, token)
        if error:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error)

        return obj

    return wrapper


def validate_sub_query(obj, token):
    validation_rules = {
        Film: validate_sub_film
    }
    return validation_rules[obj.__class__](obj, token)


def validate_sub_film(film, token):
    if film.imdb_rating < 8:
        return
    if not token:
        return 'subscription needed'
    if is_token_expired(token):
        return 'token has been expired'

    token_decoded = jwt_decode(token)
    role = token_decoded['role']
    if role not in {'admin', 'subscriber'}:
        return 'subscription needed'
