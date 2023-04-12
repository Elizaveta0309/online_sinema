import time
from datetime import datetime

import bcrypt
import jwt

from config import settings
from datetime import timezone


def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), settings.SALT).decode('utf-8')


def jwt_encode(data):
    return jwt.encode(data, settings.SECRET)


def jwt_decode(data):
    return jwt.decode(data, settings.SECRET, algorithms='HS256')


def is_token_expired(token):
    return time.mktime(datetime.now(timezone.utc).timetuple()) > jwt_decode(token)['exp']
