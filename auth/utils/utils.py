import time
from datetime import datetime
from datetime import timezone

import bcrypt
import jwt
from sqlalchemy.exc import MultipleResultsFound

from config import settings
from exceptions import Http404


def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), settings.SALT).decode('utf-8')


def jwt_encode(data):
    return jwt.encode(data, settings.SECRET)


def jwt_decode(data):
    return jwt.decode(data, settings.SECRET, algorithms='HS256')


def is_token_expired(token):
    return time.mktime(datetime.now(timezone.utc).timetuple()) > jwt_decode(token)['exp']


def get_object_or_404(model, **kwargs):
    result = model.query.filter_by(**kwargs).all()
    if len(result) > 1:
        raise MultipleResultsFound
    elif not result:
        raise Http404
    return result[0]
