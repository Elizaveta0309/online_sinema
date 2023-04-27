from functools import wraps
from http import HTTPStatus

from flask import jsonify, request
from utils.utils import is_token_expired, jwt_decode

from db.models import Role, User


def jwt_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        blacklist = kwargs.get('blacklist')
        access_token = request.cookies.get('token')
        refresh_token = request.cookies.get('refresh')

        if not (access_token and refresh_token):
            return (
                jsonify({'error': 'token is not provided'}),
                HTTPStatus.FORBIDDEN
            )

        if blacklist.is_expired(access_token) or is_token_expired(access_token):
            return (
                jsonify({'error': 'token is already blacklisted or expired'}),
                HTTPStatus.BAD_REQUEST
            )

        return f(*args, **kwargs)
    return decorator


def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.cookies.get('token')
        user_id = jwt_decode(token).get('user_id')
        user: User = User.query.filter_by(id=user_id).first()
        role = Role.query.filter_by(id=user.role).first()

        if not user:
            return jsonify({'error': 'not found'}), HTTPStatus.NOT_FOUND
        if role.title not in ['admin', 'superadmin']:
            return (
                jsonify({'error': 'admin rights required'}),
                HTTPStatus.BAD_REQUEST
            )

        return f(*args, **kwargs)
    return decorator
