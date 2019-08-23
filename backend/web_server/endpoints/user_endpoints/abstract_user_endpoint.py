from functools import wraps

from flask import session, request
from flask_restful import abort

from tools import logger
from web_server.endpoints.abstract_endpoint import AbstractEndpoint


class _UserLoginVerifier:

    @staticmethod
    def login_required(f):

        @wraps(f)
        def wrap(*args, **kwargs):

            if not _UserLoginVerifier.__is_user_authorised():
                logger.get_logger().warning("User not authorised for %s", request.path)
                return abort(403, message="Unauthorised user")

            return f(*args, **kwargs)
        return wrap

    @staticmethod
    def __is_user_authorised():

        authorised = AbstractEndpoint.USER_LOGIN_FIELD in session

        return authorised


class AbstractUserEndpoint(AbstractEndpoint):

    def __init__(self):
        super(AbstractUserEndpoint, self).__init__()
        self.method_decorators = [_UserLoginVerifier.login_required]
