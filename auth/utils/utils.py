import bcrypt

from config import settings


def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), settings.SALT).decode('utf-8')
