from werkzeug.wrappers import Response

from exceptions import NoCredsException, Http404


class ExceptionHandlerMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except NoCredsException:
            res = Response('{"error": "Нужны логин и пароль"}', mimetype='application/json', status=401)
        except Http404:
            res = Response('{"error": "Not found"}', mimetype='application/json', status=404)
        return res(environ, start_response)
