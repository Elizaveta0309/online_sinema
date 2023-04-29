from app import oauth
from config import settings


def get_social_access_url(social):
    if social == 'vk':
        response = oauth.vk.authorize_redirect(settings.OAUTH_REDIRECT_URI)
        return response.location
