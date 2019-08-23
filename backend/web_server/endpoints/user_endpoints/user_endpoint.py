from flask import session

from web_server.endpoints.abstract_endpoint import AbstractEndpoint
from web_server.endpoints.user_endpoints.abstract_user_endpoint import AbstractUserEndpoint


class UserEndpoint(AbstractUserEndpoint):

    def get(self):

        return self._create_response({
            "user_login": session[AbstractEndpoint.USER_LOGIN_FIELD]
        })
