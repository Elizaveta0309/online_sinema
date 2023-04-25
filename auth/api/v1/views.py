import flask_injector
import injector
from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import DataError

from app import app
from models import RefreshToken, Role, User, AccountEntrance
from providers import BlacklistModule, LoginRequestModule
from schemas import RoleSchema, AccountEntranceSchema
from services import LoginRequest
from utils.storage import Blacklist
from utils.utils import is_token_expired, jwt_decode, encrypt_password, get_object_or_404


@injector.inject
@app.route('/api/v1/login', methods=['POST'])
def login(login_request: LoginRequest):
    user = login_request.user
    if not user:
        return jsonify({'error': 'not found'}), 404

    if not user.check_password(login_request.password):
        return {'error': 'wrong password'}

    token, refresh = user.update_tokens()

    user.create_account_entrance()

    response = jsonify({'info': 'ok'})
    response.set_cookie('token', token)
    response.set_cookie('refresh', refresh)

    return response, 200


@injector.inject
@app.route('/api/v1/sign_up', methods=['POST'])
def sign_up(login_request: LoginRequest):
    user = login_request.user

    if user:
        return jsonify({'error': 'user with the login already exists'}), 400

    User.create(login_request.user, login_request.password)
    response = jsonify({'info': 'user created'})
    return response, 201


@app.route('/api/v1/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh')

    if not refresh_token:
        return jsonify({'error': 'no refresh token'}), 403

    user_id = jwt_decode(refresh_token).get('user_id')
    user = get_object_or_404(User, id=user_id)

    existing_refresh_token = RefreshToken.query.filter_by(token=refresh_token).first()
    if not existing_refresh_token or is_token_expired(refresh_token):
        return jsonify({'error': "token doesn't exist or expired"}), 403

    token, refresh_token_new = user.update_tokens()
    response = jsonify({'token': token, 'refresh': refresh_token_new})

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
    user = get_object_or_404(User, id=user_id)

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
def update_password(blacklist: Blacklist):
    access_token = request.cookies.get('token')
    refresh_token = request.cookies.get('refresh')
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    if not refresh_token or not access_token:
        return jsonify({'error': 'token is not provided'}), 403

    if blacklist.is_expired(access_token) or is_token_expired(access_token):
        return jsonify({'error': 'token is already blacklisted or expired'}), 400

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
            role = get_object_or_404(Role, id=role_id)
            return jsonify(RoleSchema().dump(role))
        return jsonify(RoleSchema(many=True).dump(Role.query.all()))

    def post(self):
        title = request.json.get('title')
        if Role.query.filter_by(title=title).first():
            return jsonify({'error': 'role already exists'}), 409

        Role.create(title)

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

        Role.create(title)
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
    modules=[
        BlacklistModule(),
        LoginRequestModule()
    ],
)
