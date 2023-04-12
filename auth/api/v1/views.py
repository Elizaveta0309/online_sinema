from flask import request, jsonify
from flask.views import MethodView

from app import app
from models import User, RefreshToken
from utils.utils import jwt_decode, is_token_expired


@app.route('/api/v1/login', methods=['POST'])
def login():
    login_ = request.json.get('login')
    password = request.json.get('password')
    if not (login_ and password):
        return jsonify({'error': 'нужен логин и пароль'}), 401

    user = User.query.filter_by(login=login_).first()
    if not user:
        return jsonify({'error': 'not found'}), 404

    if not user.check_password(password):
        return {'error': 'wrong password'}

    RefreshToken.query.filter_by(user=user.id).delete()

    token, refresh = user.generate_tokens()
    refresh_token = RefreshToken(token=refresh, user=user.id)
    refresh_token.save()

    response = jsonify({'info': 'ok'})
    response.set_cookie('token', token)
    response.set_cookie('refresh', refresh)

    return response, 200


@app.route('/api/v1/refresh', methods=['POST'])
def refresh():
    refresh_token = request.cookies.get('refresh')

    if not refresh_token:
        return jsonify({'error': 'no refresh token'}), 403

    user_id = jwt_decode(refresh_token).get('user_id')
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'user not found'}), 404

    existing_refresh_token = RefreshToken.query.filter_by(token=refresh_token)
    if not existing_refresh_token or is_token_expired(refresh_token):
        return jsonify({'error': "token doesn't exist or expired"}), 403

    token, refresh_token_new = user.generate_tokens()
    response = jsonify({'info': 'ok'})
    response.set_cookie('token', token)
    response.set_cookie('refresh', refresh_token_new)

    existing_refresh_token.delete()

    return response, 200
