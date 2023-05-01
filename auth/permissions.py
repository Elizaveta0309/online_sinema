from functools import wraps
from http import HTTPStatus

from flask import jsonify, request
from utils.utils import is_token_expired, jwt_decode

from db.models import Role, User

from opentelemetry import trace

tracer = trace.get_tracer(__name__)


def jwt_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        with tracer.start_as_current_span('check_jwt'):
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
        with tracer.start_as_current_span('check_role'):
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

def is_not_logged_in(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        with tracer.start_as_current_span('check_access_token'):

            token = request.cookies.get('token')
            blacklist = kwargs.get('blacklist')
            if token and not blacklist.is_expired(token):
                return jsonify({'error': 'user is already logged in'}), HTTPStatus.FORBIDDEN

            return f(*args, **kwargs)

    return decorator