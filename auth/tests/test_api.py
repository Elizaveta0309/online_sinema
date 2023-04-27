import os
import sys
from http import HTTPStatus

import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app import app
from db.models import User
from settings import test_settings


def test_login():
    with app.app_context():
        user = User.create('test_user', 'test_password')
        url = f'{test_settings.api_url}/login'
        r = requests.post(url, json={'login': 'test_user', 'password': 'test_password'})
        user.delete()
        assert r.status_code == HTTPStatus.OK


def test_non_existing_login():
    with app.app_context():
        url = f'{test_settings.api_url}/login'
        r = requests.post(url, json={'login': 'test_user', 'password': 'test_password'})
        assert r.status_code == HTTPStatus.NOT_FOUND


def test_sign_up():
    with app.app_context():
        url = f'{test_settings.api_url}/sign_up'
        r = requests.post(url, json={'login': 'test_user', 'password': 'test_password'})
        assert r.status_code == HTTPStatus.CREATED
        user = User.query.filter_by(login='test_user').first()
        try:
            assert user
        except AssertionError as e:
            raise AssertionError from e
        finally:
            user.delete()


def test_sign_up_already_exists():
    with app.app_context():
        user = User.create('test_user', 'test_password')
        url = f'{test_settings.api_url}/sign_up'
        r = requests.post(url, json={'login': 'test_user', 'password': 'test_password'})
        user.delete()
        assert r.status_code == HTTPStatus.BAD_REQUEST


def test_refresh():
    with app.app_context():
        user = User.create('test_user', 'test_password')
        url = f'{test_settings.api_url}/refresh'
        _, refresh = user.create_or_update_tokens()
        r = requests.post(url, json={'refresh': refresh})
        user.delete()
        assert r.status_code == HTTPStatus.OK


def test_refresh_empty_token():
    with app.app_context():
        url = f'{test_settings.api_url}/refresh'
        r = requests.post(url)
        assert r.status_code == HTTPStatus.BAD_REQUEST or HTTPStatus.UNSUPPORTED_MEDIA_TYPE


def test_logout():
    with app.app_context():
        user = User.create('test_user', 'test_password')
        token, refresh = user.create_or_update_tokens()
        url = f'{test_settings.api_url}/logout'
        r = requests.post(url, cookies={'token': token, 'refresh': refresh})
        user.delete()
        assert r.status_code == HTTPStatus.NO_CONTENT


def test_change_password():
    with app.app_context():
        user = User.create('test_user', 'test_password')
        url = f'{test_settings.api_url}/update_password'
        token, refresh = user.create_or_update_tokens()
        r = requests.post(
            url,
            json={'old_password': 'test_password', 'new_password': 'new_password'},
            cookies={'token': token, 'refresh': refresh}
        )

        try:
            assert user.check_password('new_password')
        except AssertionError as e:
            raise AssertionError from e
        finally:
            user.delete()

        assert r.status_code == HTTPStatus.OK


def test_change_password_wrong():
    with app.app_context():
        user = User.create('test_user', 'test_password')
        url = f'{test_settings.api_url}/update_password'
        token, refresh = user.create_or_update_tokens()
        r = requests.post(
            url,
            json={'old_password': 'test_password', 'new_password': 'new_password'},
            cookies={'token': token, 'refresh': refresh}
        )

        try:
            assert user.check_password('wrong_password')
        except AssertionError as e:
            raise AssertionError from e
        finally:
            user.delete()

        assert r.status_code == HTTPStatus.BAD_REQUEST


def test_history():
    user = User.create('test_user', 'test_password')
    url = f'{test_settings.api_url}/login'
    r = requests.post(url, json={'login': 'test_user', 'password': 'test_password'})
    token = r.cookies.get('token')
    refresh = r.cookies.get('refresh')
    url = f'{test_settings.api_url}/history'
    r = requests.post(url, cookies={'token': token, 'refresh': refresh})
    user.delete()
    assert r.status_code == HTTPStatus.OK
    assert len(r.json()['data']) == 1
