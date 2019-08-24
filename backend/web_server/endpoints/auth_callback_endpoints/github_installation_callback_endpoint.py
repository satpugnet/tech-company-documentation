from flask import session, request
from marshmallow import Schema, fields

from github_interface.interfaces.web_server_github_interface import WebServerGithubInterface
from mongo.constants.model_fields import ModelFields
from web_server.endpoints.abstract_endpoint import AbstractEndpoint


class GithubInstallationCallbackEndpoint(AbstractEndpoint):

    INSTALLATION_ID_FIELD = "installation_id"
    SETUP_ACTION_FIELD = "setup_action"

    def __init__(self):
        super().__init__()
        self._post_output_schema_instance = Schema.from_dict({
            ModelFields.GITHUB_ACCOUNT_LOGIN: fields.Str(required=True)
        })(many=True)

    def post(self):
        installation_id = request.args[self.INSTALLATION_ID_FIELD]
        setup_action = request.args[self.SETUP_ACTION_FIELD]

        installation = {}
        user_installations = WebServerGithubInterface(session[AbstractEndpoint.COOKIE_USER_LOGIN_FIELD]).request_installations()
        for user_installation in user_installations:
            if int(user_installation.id) == int(installation_id):
                installation = user_installation

        return self._create_validated_response({
            ModelFields.GITHUB_ACCOUNT_LOGIN: installation.github_account_login
        })
