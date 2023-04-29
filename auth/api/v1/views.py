from http import HTTPStatus

import flask_injector
import injector
import requests
from flasgger import swag_from
from flask import jsonify, request
from flask.views import MethodView

from app import app
from db.models import RefreshToken, Role, User, UserSocial
from permissions import jwt_required, admin_required
from providers import BlacklistModule, LoginRequestModule
from schemas import RoleSchema, AccountEntranceSchema
from services import LoginRequest
from socials import get_social_access_url
from utils.storage import Blacklist
from utils.utils import is_token_expired, jwt_decode, encrypt_password, get_object_or_404

flask_injector.FlaskInjector(
    app=app,
    modules=[
        BlacklistModule(),
        LoginRequestModule()
    ],
)


@injector.inject
@app.route('/api/v1/login', methods=['POST'])
@swag_from('docs/login.yaml')
def login(login_request: LoginRequest):
    user = login_request.user
    if not user:
        return jsonify({'error': 'not found'}), HTTPStatus.NOT_FOUND

    if not user.check_password(login_request.password):
        return {'error': 'wrong password'}

    token, refresh = user.create_or_update_tokens()

    user.create_account_entrance()

    response = jsonify({'info': 'ok'})
    response.set_cookie('token', token)
    response.set_cookie('refresh', refresh)

    return response, HTTPStatus.OK


@injector.inject
@app.route('/api/v1/sign_up', methods=['POST'])
@swag_from('docs/sign_up.yaml')
def sign_up(login_request: LoginRequest):
    user = login_request.user

    if user:
        return jsonify({'error': 'user with the login already exists'}), HTTPStatus.BAD_REQUEST

    User.create(login_request.login, login_request.password)
    response = jsonify({'info': 'user created'})
    return response, HTTPStatus.CREATED


@app.route('/api/v1/refresh', methods=['POST'])
@swag_from('docs/refresh.yaml')
def refresh():
    refresh_token = request.json.get('refresh')

    if not refresh_token:
        return jsonify({'error': 'no refresh token'}), HTTPStatus.FORBIDDEN

    user_id = jwt_decode(refresh_token).get('user_id')
    user = get_object_or_404(User, id=user_id)

    existing_refresh_token = RefreshToken.query.filter_by(token=refresh_token).first()
    if not existing_refresh_token or is_token_expired(refresh_token):
        return jsonify({'error': "token doesn't exist or expired"}), HTTPStatus.FORBIDDEN

    token, refresh_token_new = user.update_tokens()
    response = jsonify({'token': token, 'refresh': refresh_token_new})

    return response, HTTPStatus.OK


@injector.inject
@app.route('/api/v1/logout', methods=['POST'])
@jwt_required
@swag_from('docs/logout.yaml')
def logout(blacklist: Blacklist):
    access_token = request.cookies.get('token')
    refresh_token = request.cookies.get('refresh')

    user_id = jwt_decode(refresh_token).get('user_id')
    user = get_object_or_404(User, id=user_id)

    RefreshToken.query.filter_by(user=user.id).delete()
    blacklist.add_to_expired(access_token)

    return (
        jsonify({"info": "Access token revoked"}),
        HTTPStatus.NO_CONTENT
    )


@injector.inject
@app.route('/api/v1/update_password', methods=['POST'])
@jwt_required
@swag_from('docs/update_password.yaml')
def update_password(blacklist: Blacklist):
    access_token = request.cookies.get('token')
    refresh_token = request.cookies.get('refresh')
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    if not refresh_token or not access_token:
        return jsonify({'error': 'token is not provided'}), HTTPStatus.FORBIDDEN

    if blacklist.is_expired(access_token) or is_token_expired(access_token):
        return jsonify({'error': 'token is already blacklisted or expired'}), HTTPStatus.BAD_REQUEST

    user_id = jwt_decode(refresh_token).get('user_id')
    user = get_object_or_404(User, id=user_id)

    if not user.check_password(old_password):
        return jsonify({'error': 'wrong password'}), HTTPStatus.BAD_REQUEST

    if user.check_password(new_password):
        return {'error': 'new password should be different'}, HTTPStatus.BAD_REQUEST

    user.password = encrypt_password(new_password)
    user.save()

    RefreshToken.query.filter_by(user=user.id).delete()
    blacklist.add_to_expired(access_token)

    return jsonify({'info': 'password refreshed'}), HTTPStatus.OK


@app.route('/api/v1/history', methods=['POST'])
@jwt_required
@swag_from('docs/history.yaml')
def history():
    access_token = request.cookies.get('token')

    user_id = jwt_decode(access_token).get('user_id')
    user = get_object_or_404(User, id=user_id)

    account_entrances = user.get_account_entrances()
    total_entries = account_entrances.count()

    page = int(request.args.get('page', 1))
    limit = int(request.args.get('per_page', 10))

    offset = (page - 1) * limit

    account_entrances = account_entrances.offset(offset).limit(limit)

    if not account_entrances:
        return jsonify({'error': 'no sessions found'}), HTTPStatus.NOT_FOUND

    return (
        jsonify({
            'data': AccountEntranceSchema(many=True).dump(account_entrances),
            'total_entries': total_entries,
            'page': page,
            'per_page': limit
        }),
        HTTPStatus.OK
    )


class RoleView(MethodView):
    def get(self, role_id=None):
        """
          ---
          tags:
          - get a role or all roles
          parameters:
          - name: access_token
            in: cookie
            required: True
            type: 'string'
          - name: role_id
            in: path
            required: False
            type: 'string'
          responses:
             200:
               description: Role by id
               schema:
                  $reper_pagef: '#/definitions/Role'
             404:
               description: Role not found
        """
        if role_id:
            role = get_object_or_404(Role, id=role_id)
            return jsonify(RoleSchema().dump(role))
        return jsonify(RoleSchema(many=True).dump(Role.query.all()))

    @admin_required
    def post(self):
        """
             Create a role
             ---
             tags:
             - create role
             parameters:
             - name: access_token
               in: cookie
               required: True
               type: 'string'
             - name: title
               in: body
               required: True
               type: 'string'
             responses:
                201:
                  description: id of the new role
                  schema:
                    $ref: '#/definitions/RoleID'
                400:
                  description: admin rights required
                409:
                  description: Role already exists
        """
        title = request.json.get('title')
        if Role.query.filter_by(title=title).first():
            return jsonify({'error': 'role already exists'}), HTTPStatus.CONFLICT

        r = Role.create(title)

        return jsonify({'id': str(r.id)}), HTTPStatus.CREATED

    @admin_required
    def patch(self, role_id):
        """
             Update title of role
             ---
             tags:
             - update role
             parameters:
             - name: access_token
               in: cookie
               required: True
               type: 'string'
             - name: title
               in: body
               required: True
               type: 'string'
             - name: role_id
               in: path
               required: True
               type: 'string'
             responses:
                200:
                  description: Role was updated
                  schema:
                    $ref: '#/definitions/SuccessInfo'
                400:
                  description: admin rights required
                403:
                  description: Title was not provided
                404:
                  description: Role not found

        """

        title = request.json.get('title')
        if not title:
            return jsonify({'error': "title wasn't provided"}), HTTPStatus.FORBIDDEN

        role = get_object_or_404(Role, id=role_id)
        role.title = title
        role.save()
        return jsonify({'info': 'ok'}), HTTPStatus.OK

    @admin_required
    def delete(self, role_id):
        """
             Delete a role by id
             ---
             tags:
             - delete a role
             parameters:
             - name: access_token
               in: cookie
               required: True
               type: 'string'
             - name: role_id
               in: path
               required: True
               type: 'string'
             responses:
                200:
                  description: Role was updated
                  schema:
                    $ref: '#/definitions/SuccessInfo'
                400:
                  description: admin rights required
                404:
                  description: Role not found
        """
        role = get_object_or_404(Role, id=role_id)
        role.delete()
        return jsonify({'info': 'ok'}), HTTPStatus.OK


role_view = RoleView.as_view('role_api')
app.add_url_rule('/api/v1/roles/',
                 view_func=role_view, methods=['GET', 'POST'])
app.add_url_rule('/api/v1/roles/<role_id>',
                 view_func=role_view, methods=['GET', 'PATCH', 'DELETE'])


@app.route('/api/v1/oauth_vk', methods=['POST'])
def oauth():
    social = request.args.get('social')
    if not social:
        return jsonify({'error': 'please provide social type'}), HTTPStatus.FORBIDDEN
    social_access_url = get_social_access_url(social)
    return jsonify({'url': social_access_url})


@app.route('/api/v1/callback')
def callback():
    a = request
    code = request.args['code']
    # url = f'https://oauth.vk.com/access_token/'
    url = f'https://oauth.vk.com/access_token?client_id=51629723&client_secret=NgRvwx5YoYGauO39VANy&code={code}&redirect_uri=http%3A%2F%2F3a17-46-138-168-89.ngrok-free.app%2Fapi%2Fv1%2Fcallback'
    data = requests.get(url).json()
    access_token = data.get('access_token', '')
    if access_token.startswith('vk1'):
        social_user_id = str(data['user_id'])

        if user_social := UserSocial.query.filter_by(social_user_id=social_user_id).first():
            user = User.query.filter_by(id=user_social.user).first()
        else:
            user = User.create(social_user_id, 'social')
            UserSocial.create(user=user.id, social_user_id=social_user_id)

        token, refresh = user.create_or_update_tokens()
        user.create_account_entrance()
        response = jsonify({'info': 'ok'})
        response.set_cookie('token', token)
        response.set_cookie('refresh', refresh)
        return response, HTTPStatus.OK
