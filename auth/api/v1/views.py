from datetime import datetime, timezone

import flask_injector
import injector
from app import app
from flask import jsonify, request
from flask.views import MethodView
from providers import BlacklistModule
from schemas import RoleSchema
from sqlalchemy.exc import DataError
from utils.storage import Blacklist
from utils.utils import is_token_expired, jwt_decode

from models import RefreshToken, Role, User, UserSession


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

    session = UserSession(user=user.id, isActive=True, creation_date=datetime.now(timezone.utc))
    session.save()

    response = jsonify({'info': 'ok'})
    response.set_cookie('token', token)
    response.set_cookie('refresh', refresh)

    return response, 200


@app.route('/api/v1/sign_up', methods=['POST'])
def sign_up():
    login_ = request.json.get('login')
    password = request.json.get('password')
    if not (login_ and password):
        return jsonify({'error': 'нужен логин и пароль'}), 401

    user = User.query.filter_by(login=login_).first()
    if user:
        return jsonify({'error': 'user with the login already exists'}), 400

    user = User(login_, password)
    user.save()

    response = jsonify({'info': 'user created'})

    return response, 201


@app.route('/api/v1/refresh', methods=['POST'])
def refresh():
    refresh_token = request.cookies.get('refresh')

    if not refresh_token:
        return jsonify({'error': 'no refresh token'}), 403

    user_id = jwt_decode(refresh_token).get('user_id')
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'user not found'}), 404

    existing_refresh_token = RefreshToken.query.filter_by(token=refresh_token).first()
    if not existing_refresh_token or is_token_expired(refresh_token):
        return jsonify({'error': "token doesn't exist or expired"}), 403

    token, refresh_token_new = user.generate_tokens()
    response = jsonify({'info': 'ok'})
    response.set_cookie('token', token)
    response.set_cookie('refresh', refresh_token_new)

    existing_refresh_token.delete()

    return response, 200


@injector.inject
@app.route('/api/v1/logout', methods=['POST'])
def logout(blacklist: Blacklist):
    access_token = request.cookies.get('token')
    refresh_token = request.cookies.get('refresh')

    if not refresh_token or not access_token:
        return jsonify({'error': 'token is not provided'}), 403

    if blacklist.is_expired(access_token) or is_token_expired(access_token):
        return jsonify({'error': 'token is already blacklisted or expired'}), 400

    user_id = jwt_decode(refresh_token).get('user_id')
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'user not found'}), 404

    RefreshToken.query.filter_by(user=user.id).delete()
    blacklist.add_to_expired(access_token)

    session = UserSession.query.filter_by(user=user.id).first()
    session.isActive = False
    session.save()

    return (
        jsonify({"info": "Access token revoked"}),
        204
    )


@app.route('/api/v1/history', methods=['POST'])
def history(blacklist: Blacklist):
    access_token = request.cookies.get('token')

    if not access_token:
        return jsonify({'error': 'access token is not provided'}), 403

    if blacklist.is_expired(access_token) or is_token_expired(access_token):
        return jsonify({'error': 'token is already blacklisted or expired'}), 400

    user_id = jwt_decode(access_token).get('user_id')
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'user not found'}), 404

    user_sessions = UserSession.query.filter_by(user=user.id).all()

    if not user_sessions:
        return jsonify({'error': 'no session found'}), 404

    return (
        jsonify({"history": user_sessions}),
        200
    )


class RoleView(MethodView):
    def get(self, role_id=None):
        if role_id:
            try:
                role = Role.query.filter_by(id=role_id).first()
            except DataError:
                role = None

            if not role:
                return jsonify({'error': 'not found'}), 404

            return jsonify(RoleSchema().dump(role))

        return jsonify(RoleSchema(many=True).dump(Role.query.all()))

    def post(self):
        title = request.json.get('title')
        if Role.query.filter_by(title=title).first():
            return jsonify({'error': 'role already exists'}), 409

        r = Role(title)
        r.save()

        return jsonify({'id': str(r.id)}), 201

    def patch(self, role_id):
        try:
            role = Role.query.filter_by(id=role_id).first()
        except DataError:
            role = None
        if not role:
            return jsonify({'error': 'not found'}), 404

        title = request.json.get('title')
        if not title:
            return jsonify({'error': "title wasn't provided"})

        role.title = title
        role.save()

        return jsonify({'info': 'ok'}), 200

    def delete(self, role_id):
        try:
            role = Role.query.filter_by(id=role_id).first()
        except DataError:
            role = None

        if not role:
            return jsonify({'error': 'not found'}), 404

        role.delete()

        return jsonify({'info': 'ok'}), 200


role_view = RoleView.as_view('role_api')
app.add_url_rule('/api/v1/roles/',
                 view_func=role_view, methods=['GET', 'POST'])
app.add_url_rule('/api/v1/roles/<role_id>',
                 view_func=role_view, methods=['GET', 'PATCH', 'DELETE'])

flask_injector.FlaskInjector(
    app=app,
    modules=[BlacklistModule()],
)
