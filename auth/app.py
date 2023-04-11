from flask import Flask, request, jsonify

from db import init_db
from models import User

app = Flask(__name__)


@app.route('/login', methods=['POST'])
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

    response = jsonify({'token': token, 'refresh': refresh})
    response.set_cookie('token', token)
    response.set_cookie('refresh', refresh)

    return response


def main():
    init_db()


if __name__ == '__main__':
    main()
