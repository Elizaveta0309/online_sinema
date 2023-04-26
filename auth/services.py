from flask import request, jsonify
from sqlalchemy.exc import ProgrammingError

from exceptions import NoCredsException
from models import User


class LoginRequest:
    def __init__(self):
        self.login = request.json.get('login')
        self.password = request.json.get('password')

        try:
            self.user = User.query.filter_by(login=self.login).first() if self.login else None
        except ProgrammingError:
            self.user = None

        self.validate_cred()

    def validate_cred(self):
        if not (self.login and self.password):
            raise NoCredsException
