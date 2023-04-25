from datetime import datetime, timezone
from functools import wraps
from http import HTTPStatus

import flask_injector
import injector
from flask import jsonify, request
from flask.views import MethodView

from app import app
from providers import BlacklistModule
from schemas import RoleSchema, AccountEntranceSchema
from sqlalchemy.exc import DataError
from utils.storage import Blacklist

from utils.utils import is_token_expired, jwt_decode, encrypt_password
from models import RefreshToken, Role, User, AccountEntrance
from permissions import jwt_required, admin_required


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

    entrance = AccountEntrance(user=user.id, entrance_date=datetime.now(timezone.utc))
    entrance.save()

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
    refresh_token = request.json.get('refresh')

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
    response = jsonify({'token': token, 'refresh': refresh_token_new})

    existing_refresh_token.delete()
    rt = RefreshToken(token=refresh_token_new, user=user.id)
    rt.save()

    return response, 200


@injector.inject
@app.route('/api/v1/logout', methods=['POST'])
@jwt_required
def logout(blacklist: Blacklist):
    access_token = request.cookies.get('token')
    refresh_token = request.cookies.get('refresh')

    user_id = jwt_decode(refresh_token).get('user_id')
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'user not found'}), 404

    RefreshToken.query.filter_by(user=user.id).delete()
    blacklist.add_to_expired(access_token)

    return (
        jsonify({"info": "Access token revoked"}),
        204
    )


@injector.inject
@app.route('/api/v1/update_password', methods=['POST'])
@jwt_required
def update_password(blacklist: Blacklist):
    access_token = request.cookies.get('token')
    refresh_token = request.cookies.get('refresh')
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    user_id = jwt_decode(refresh_token).get('user_id')
    user: User = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'user not found'}), 404

    if not user.check_password(old_password):
        return jsonify({'error': 'wrong password'}), 400

    if user.check_password(new_password):
        return {'error': 'new password should be different'}, 400

    user.password = encrypt_password(new_password)
    user.save()

    RefreshToken.query.filter_by(user=user.id).delete()
    blacklist.add_to_expired(access_token)

    return jsonify({'info': 'password refreshed'}), 200


@app.route('/api/v1/history', methods=['POST'])
@jwt_required
def history(blacklist: Blacklist):
    access_token = request.cookies.get('token')

    user_id = jwt_decode(access_token).get('user_id')
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'user not found'}), 404

    account_entrances = AccountEntrance.query.filter_by(user=user.id)
    total_entries = account_entrances.count()

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    offset = (page - 1) * per_page
    limit = per_page

    account_entrances = account_entrances.offset(offset).limit(limit)

    if not account_entrances:
        return jsonify({'error': 'no sessions found'}), 404

    return (
        jsonify({
            'data': AccountEntranceSchema(many=True).dump(account_entrances),
            'total_entries': total_entries,
            'page': page,
            'per_page': per_page
        }),
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

    @admin_required
    def post(self):
        title = request.json.get('title')
        if Role.query.filter_by(title=title).first():
            return jsonify({'error': 'role already exists'}), 409

        r = Role(title)
        r.save()

        return jsonify({'id': str(r.id)}), 201

    @admin_required
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

    @admin_required
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
