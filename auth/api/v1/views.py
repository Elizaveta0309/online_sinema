from flask import request, jsonify

from app import app
from models import User, RefreshToken


@app.route('/api/v1/login', methods=['POST'])
def login():
    login_ = request.json.get('login')
    password = request.json.get('password')
    if not (login_ and password):
        return {'error': 'нужен логин и пароль'}  # TODO заменить на верификацию marshmallow

    user = User.query.filter_by(login=login_).first()
    if not user:
        return {'error': 'not found'}

    if not user.check_password(password):
        return {'error': 'wrong password'}

    token, refresh = user.generate_tokens()
    refresh_token = RefreshToken(token=refresh)
    refresh_token.save()

    response = jsonify({'token': token, 'refresh': refresh})
    response.set_cookie('token', token)
    response.set_cookie('refresh', refresh)

    return response
