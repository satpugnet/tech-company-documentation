import uuid

from flask import request, session
from marshmallow import Schema, fields

from github_interface.interfaces.web_server_github_interface import WebServerGithubInterface
from mongo.constants.model_fields import ModelFields
from utils.code_formatter import CodeFormatter
from web_server.endpoints.abstract_endpoint import AbstractEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountLinesEndpoint(AbstractAccountEndpoint):
    """
    Endpoint for handling the code lines.
    """

    def __init__(self):
        super().__init__()
        self._get_output_schema_instance = Schema.from_dict({
            ModelFields.ID: fields.UUID(required=True),
            ModelFields.CODE: fields.Str(required=True)
        })()

    def get(self, github_account_login):

        repo_name = request.args[ModelFields.REPO_NAME]
        path = request.args[ModelFields.PATH]
        start_line = int(request.args[ModelFields.START_LINE])
        end_line = int(request.args[ModelFields.END_LINE])

        repo_interface = WebServerGithubInterface(session[AbstractEndpoint.COOKIE_USER_LOGIN_FIELD]).request_repo(github_account_login, repo_name)

        fs_node = repo_interface.get_fs_node_at_path(path)
        content = ''.join(fs_node.content.splitlines(keepends=True)[start_line - 1: end_line])

        code = CodeFormatter().format(path, content, start_line)

        return self._create_validated_response({
            ModelFields.ID: str(uuid.uuid1()),  # generate a unique id for the reference
            ModelFields.CODE: code
        })
