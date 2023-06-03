from abc import ABC, abstractmethod

import requests
from app import oauth
from config import settings
from flask import jsonify, request
from utils.utils import generate_random_password

from db.models import User, UserSocial


def get_social_access_url(social):
    if social == 'vk':
        response = oauth.vk.authorize_redirect(settings.VK_REDIRECT_URI)
        return response.location


class OAuthProvider(ABC):
    def __init__(self, name, authorize_url, access_token_url, client_id, client_secret):
        self.name = name
        self.authorize_url = authorize_url
        self.access_token_url = access_token_url
        self.client_id = client_id
        self.client_secret = client_secret

        oauth.register(
            name=name,
            authorize_url=authorize_url,
            access_token_url=access_token_url,
            client_id=client_id,
            client_secret=client_secret
        )

    @abstractmethod
    def generate_authorize_url(self):
        ...

    @abstractmethod
    def authorize(self):
        ...


class OAuthProviderVK(OAuthProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oauth = oauth.vk
        self.redirect_uri = f'{settings.OAUTH_REDIRECT_URI}/vk'

    def generate_authorize_url(self):
        response = self.oauth.authorize_redirect(self.redirect_uri)
        return response.location

    def get_access_token_url(self, code):
        return f'{self.access_token_url}?client_id={self.client_id}' \
               f'&client_secret={settings.VK_ACCESS_TOKEN}&code={code}&redirect_uri={self.redirect_uri}'

    @staticmethod
    def get_or_create_user(social_user_id):
        if user_social := UserSocial.query.filter_by(social_user_id=social_user_id).first():
            user = User.query.filter_by(id=user_social.user).first()
        else:
            user = User.create(social_user_id, generate_random_password())
            UserSocial.create(user=user.id, social_user_id=social_user_id)
        return user

    @staticmethod
    def get_response(user, request):
        ip_addr = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        token, refresh = user.create_or_update_tokens()
        user.create_account_entrance(user_agent, ip_addr, 'vk')
        response = jsonify({'info': 'ok'})
        response.set_cookie('token', token)
        response.set_cookie('refresh', refresh)
        return response

    def authorize(self):
        code = request.args['code']
        url = self.get_access_token_url(code)
        data = requests.get(url).json()

        if 'access_token' not in data:
            return jsonify({'error': 'authorization error'})

        social_user_id = str(data['user_id'])
        user = self.get_or_create_user(social_user_id)

        return self.get_response(user, request)


vk_provider = OAuthProviderVK(
    name='vk',
    authorize_url=settings.VK_AUTHORIZE_URL,
    access_token_url=settings.VK_ACCESS_TOKEN_URL,
    client_id=settings.VK_CLIENT_ID,
    client_secret=settings.VK_ACCESS_TOKEN
)


def get_provider(provider_id):
    providers = {
        'vk': vk_provider
    }
    try:
        return providers[provider_id]
    except KeyError:
        return
