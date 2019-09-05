from flask import session
from marshmallow import Schema, fields

from github_interface.interfaces.web_server_github_interface import WebServerGithubInterface
from mongo.constants.model_fields import ModelFields
from web_server.endpoints.abstract_endpoint import AbstractEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountReposEndpoint(AbstractAccountEndpoint):
    """
    Endpoint for handling the repos.
    """

    def __init__(self):
        super().__init__()
        self._get_output_schema_instance = Schema.from_dict({
            ModelFields.GITHUB_ACCOUNT_LOGIN: fields.Str(required=True),
            ModelFields.NAME: fields.Str(required=True)
        })(many=True)

    def get(self, github_account_login):

        repo_interfaces = WebServerGithubInterface(session[AbstractEndpoint.COOKIE_USER_LOGIN_FIELD]).request_repos(github_account_login)

        return self._create_validated_response([repo_interface.repo for repo_interface in repo_interfaces])
