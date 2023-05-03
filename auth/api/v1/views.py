from http import HTTPStatus

import flask_injector
import injector
from flasgger import swag_from
from flask import jsonify, request
from flask.views import MethodView
from opentelemetry import trace

from app import app
from db.models import RefreshToken, Role, User
from permissions import jwt_required, admin_required, is_not_logged_in
from providers import BlacklistModule, LoginRequestModule
from schemas import RoleSchema, AccountEntranceSchema
from services import LoginRequest
from socials import get_provider
from utils.storage import Blacklist
from utils.utils import is_token_expired, jwt_decode, encrypt_password, get_object_or_404

tracer = trace.get_tracer(__name__)


@injector.inject
@app.route('/api/v1/login', methods=['POST'])
@is_not_logged_in
@swag_from('docs/login.yaml')
def login(login_request: LoginRequest, blacklist: Blacklist):
    with tracer.start_as_current_span('login') as login:
        ip_addr = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        request_id = request.headers.get('X-Request-Id')
        login.set_attribute('http.request_id', request_id)

        with tracer.start_as_current_span('query_for_user'):
            user = login_request.user
            if not user:
                return jsonify({'error': 'not found'}), HTTPStatus.NOT_FOUND

            if not user.check_password(login_request.password):
                return {'error': 'wrong password'}, HTTPStatus.FORBIDDEN

        with tracer.start_as_current_span('work_with_tokens'):
            token, refresh = user.create_or_update_tokens()

        with tracer.start_as_current_span('save_account_entrance'):
            user.create_account_entrance(user_agent, ip_addr)

        response = jsonify({'info': 'ok', 'token': token, 'refresh': refresh})
        response.set_cookie('token', token)
        response.set_cookie('refresh', refresh)

        return response, HTTPStatus.OK


@injector.inject
@app.route('/api/v1/sign_up', methods=['POST'])
@swag_from('docs/sign_up.yaml')
def sign_up(login_request: LoginRequest):
    with tracer.start_as_current_span('sign_up') as sign_up:
        request_id = request.headers.get('X-Request-Id')
        sign_up.set_attribute('http.request_id', request_id)

        with tracer.start_as_current_span('check_user'):
            user = login_request.user

            if user:
                return jsonify({'error': 'user with the login already exists'}), HTTPStatus.BAD_REQUEST

        with tracer.start_as_current_span('create_user'):
            User.create(login_request.login, login_request.password)

        response = jsonify({'info': 'user created'})
        return response, HTTPStatus.CREATED


@app.route('/api/v1/refresh', methods=['POST'])
@swag_from('docs/refresh.yaml')
def refresh():
    with tracer.start_as_current_span('refresh') as refresh:

        request_id = request.headers.get('X-Request-Id')
        refresh.set_attribute('http.request_id', request_id)

        with tracer.start_as_current_span('check_refresh'):
            refresh_token = request.json.get('refresh')

            if not refresh_token:
                return jsonify({'error': 'no refresh token'}), HTTPStatus.FORBIDDEN

            existing_refresh_token = RefreshToken.query.filter_by(token=refresh_token).first()
            if not existing_refresh_token or is_token_expired(refresh_token):
                return jsonify({'error': "token doesn't exist or expired"}), HTTPStatus.FORBIDDEN

        with tracer.start_as_current_span('check_user'):
            user_id = jwt_decode(refresh_token).get('user_id')
            user = get_object_or_404(User, id=user_id)

        with tracer.start_as_current_span('issue_tokens'):
            token, refresh_token_new = user.create_or_update_tokens()

        response = jsonify({'token': token, 'refresh': refresh_token_new})
        return response, HTTPStatus.OK


@injector.inject
@app.route('/api/v1/logout', methods=['POST'])
@jwt_required
@swag_from('docs/logout.yaml')
def logout(blacklist: Blacklist):
    with tracer.start_as_current_span('logout') as logout:
        request_id = request.headers.get('X-Request-Id')
        logout.set_attribute('http.request_id', request_id)

        access_token = request.cookies.get('token')
        refresh_token = request.cookies.get('refresh')

        with tracer.start_as_current_span('check_user'):
            user_id = jwt_decode(refresh_token).get('user_id')
            user = get_object_or_404(User, id=user_id)

        with tracer.start_as_current_span('add_token_to_blacklist'):
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
    with tracer.start_as_current_span('update_password') as update_password:

        request_id = request.headers.get('X-Request-Id')
        update_password.set_attribute('http.request_id', request_id)

        access_token = request.cookies.get('token')
        refresh_token = request.cookies.get('refresh')
        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')

        with tracer.start_as_current_span('check_user'):
            user_id = jwt_decode(refresh_token).get('user_id')
            user = get_object_or_404(User, id=user_id)

        with tracer.start_as_current_span('check_passwords'):
            if not user.check_password(old_password):
                return jsonify({'error': 'wrong password'}), HTTPStatus.BAD_REQUEST

            if user.check_password(new_password):
                return {'error': 'new password should be different'}, HTTPStatus.BAD_REQUEST

        with tracer.start_as_current_span('save_to_postgres'):
            user.password = encrypt_password(new_password)
            user.save()

        with tracer.start_as_current_span('get rid of tokens'):
            RefreshToken.query.filter_by(user=user.id).delete()
            blacklist.add_to_expired(access_token)

        return jsonify({'info': 'password refreshed'}), HTTPStatus.OK


@app.route('/api/v1/history', methods=['POST'])
@jwt_required
@swag_from('docs/history.yaml')
def history(blacklist: Blacklist):
    with tracer.start_as_current_span('history') as history:
        request_id = request.headers.get('X-Request-Id')
        history.set_attribute('http.request_id', request_id)

        access_token = request.cookies.get('token')

        with tracer.start_as_current_span('check_user'):
            user_id = jwt_decode(access_token).get('user_id')
            user = get_object_or_404(User, id=user_id)

        with tracer.start_as_current_span('get_from_postgres'):
            account_entrances = user.get_account_entrances()
            total_entries = account_entrances.count()
            if not account_entrances:
                return jsonify({'error': 'no sessions found'}), HTTPStatus.NOT_FOUND

        page = int(request.args.get('page', 1))
        limit = int(request.args.get('per_page', 10))

        offset = (page - 1) * limit

        account_entrances = account_entrances.offset(offset).limit(limit)

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
    @admin_required
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
                  $ref: '#/definitions/Role'
             404:
               description: Role not found
        """
        with tracer.start_as_current_span('role') as role:
            request_id = request.headers.get('X-Request-Id')
            role.set_attribute('http.request_id', request_id)

            with tracer.start_as_current_span('get_role'):
                if role_id:
                    role = get_object_or_404(Role, id=role_id)
                    return jsonify(RoleSchema().dump(role))
            with tracer.start_as_current_span('get_roles'):
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
               schema:
                 $ref: '#/definitions/RoleTitle'
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
        with tracer.start_as_current_span('create_role') as create_role:
            request_id = request.headers.get('X-Request-Id')
            create_role.set_attribute('http.request_id', request_id)

            with tracer.start_as_current_span('query_to_postgres'):
                title = request.json.get('title')
                if Role.query.filter_by(title=title).first():
                    return jsonify({'error': 'role already exists'}), HTTPStatus.CONFLICT

            with tracer.start_as_current_span('save_to_postgres'):
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
               schema:
                 $ref: '#/definitions/RoleTitle'
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
        with tracer.start_as_current_span('update_role') as update_role:
            request_id = request.headers.get('X-Request-Id')
            update_role.set_attribute('http.request_id', request_id)

            with tracer.start_as_current_span('query_to_postgres'):
                title = request.json.get('title')
                if not title:
                    return jsonify({'error': "title wasn't provided"})

                role = get_object_or_404(Role, id=role_id)

            with tracer.start_as_current_span('save_to_postgres'):
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
        with tracer.start_as_current_span('delete_role') as update_role:
            request_id = request.headers.get('X-Request-Id')
            update_role.set_attribute('http.request_id', request_id)

            with tracer.start_as_current_span('query_to_postgres'):
                role = get_object_or_404(Role, id=role_id)
            with tracer.start_as_current_span('delete_from_postgres'):
                role.delete()
                return jsonify({'info': 'ok'}), HTTPStatus.OK


role_view = RoleView.as_view('role_api')
app.add_url_rule('/api/v1/roles/',
                 view_func=role_view, methods=['GET', 'POST'])
app.add_url_rule('/api/v1/roles/<role_id>',
                 view_func=role_view, methods=['GET', 'PATCH', 'DELETE'])

flask_injector.FlaskInjector(
    app=app,
    modules=[
        BlacklistModule(),
        LoginRequestModule()
    ],
)


@app.route('/api/v1/oauth', methods=['GET'])
def oauth():
    provider_id = request.args.get('provider_id')

    if not provider_id:
        return jsonify({'error': 'please provide provider type'}), HTTPStatus.FORBIDDEN
    provider = get_provider(provider_id)

    if not provider:
        return jsonify({'error': 'provider not found'})

    social_access_url = provider.generate_authorize_url()
    return jsonify({'url': social_access_url})


@app.route('/api/v1/callback/<provider_id>', methods=['GET'])
def callback(provider_id):
    provider = get_provider(provider_id)
    return provider.authorize() if provider else jsonify({'error': 'provider not found'})
