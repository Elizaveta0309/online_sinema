from uuid import uuid4

import bcrypt
import jwt
from config import settings
from exceptions import Http404
from jwt import ExpiredSignatureError, InvalidSignatureError
from sqlalchemy.exc import MultipleResultsFound


def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), settings.SALT).decode('utf-8')


def jwt_encode(data):
    return jwt.encode(data, settings.SECRET)


def jwt_decode(data):
    return jwt.decode(data, settings.SECRET, algorithms='HS256')


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


def get_object_or_404(model, **kwargs):
    result = model.query.filter_by(**kwargs).all()
    if len(result) > 1:
        raise MultipleResultsFound
    elif not result:
        raise Http404
    return result[0]


def generate_random_password():
    return str(uuid4())
