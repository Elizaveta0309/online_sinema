import os
import sys

import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app import app
from settings import test_settings

from db.models import Role, User


def test_get():
    with app.app_context():
        url = f'{test_settings.api_url}/roles'
        role = Role.create('test_role')
        data = requests.get(url).json()
        role.delete()
        assert len(data) > 1


def test_get_by_id():
    with app.app_context():
        role = Role.create('test_role')
        url = f'{test_settings.api_url}/roles/{role.id}'
        data = requests.get(url).json()
        role.delete()
        assert data


def test_create():
    with app.app_context():
        url = f'{test_settings.api_url}/roles'
        Role.query.filter_by(title='admin').first() or Role.create('admin')
        user = User.create('test_admin', 'test_password', 'admin')
        token, refresh = user.create_or_update_tokens()

        data = requests.post(
            url,
            json={'title': 'test_role'},
            cookies={'token': token, 'refresh': refresh}
        ).json()

        Role.query.filter_by(id=data['id']).delete()
        user.delete()

        assert data


def test_update():
    with app.app_context():
        role = Role.create('test_role')
        url = f'{test_settings.api_url}/roles/{role.id}'
        Role.query.filter_by(title='admin').first() or Role.create('admin')
        user = User.create('test_admin', 'test_password', 'admin')
        token, refresh = user.create_or_update_tokens()

        requests.patch(
            url,
            json={'title': 'test_role_new'},
            cookies={'token': token, 'refresh': refresh}
        ).json()

        role = Role.query.filter_by(id=role.id).first()
        title = role.title
        role.delete()
        user.delete()

        assert title == 'test_role_new'


def test_delete():
    with app.app_context():
        role = Role.create('test_role')
        url = f'{test_settings.api_url}/roles/{role.id}'
        Role.query.filter_by(title='admin').first() or Role.create('admin')
        user = User.create('test_admin', 'test_password', 'admin')
        token, refresh = user.create_or_update_tokens()
        role_id = role.id

        requests.delete(
            url,
            json={'title': 'test_role'},
            cookies={'token': token, 'refresh': refresh}
        ).json()

        user.delete()

        try:
            assert not Role.query.filter_by(id=role_id).first()
        except AssertionError as e:
            role.delete()
            raise AssertionError from e
