from flask import session

from web_server.endpoints.abstract_endpoint import AbstractEndpoint


class UserLogoutEndpoint(AbstractEndpoint):

    def delete(self):
        session.pop(AbstractEndpoint.USER_LOGIN_FIELD)

        return self._create_response({})
