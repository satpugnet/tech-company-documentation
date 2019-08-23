from flask import session

from github_interface.interfaces.authenticated_github_interface import AuthenticatedGithubInterface
from mongo.constants.db_fields import ModelFields
from web_server.endpoints.abstract_endpoint import AbstractEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountReposEndpoint(AbstractAccountEndpoint):

    def get(self, github_account_login):

        # Get the repository list
        repo_names = []
        for repo_interface in AuthenticatedGithubInterface(session[AbstractEndpoint.USER_LOGIN_FIELD]).request_repos(github_account_login):
            repo_names.append({ModelFields.NAME: repo_interface.repo.name,
                               ModelFields.GITHUB_ACCOUNT_LOGIN: repo_interface.repo.github_account_login})

        # Return the response
        return self._create_response(repo_names)
