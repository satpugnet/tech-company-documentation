from flask import session

from github_interface.interfaces.authenticated_github_interface import AuthenticatedGithubInterface
from web_server.endpoints.abstract_endpoint import AbstractEndpoint
from web_server.endpoints.user_endpoints.abstract_user_endpoint import AbstractUserEndpoint


class UserInstallsEndpoint(AbstractUserEndpoint):

    def get(self):
        user_installations = AuthenticatedGithubInterface(session[AbstractEndpoint.USER_LOGIN_FIELD]).request_installations()

        return self._create_response(user_installations)
