from flask import session, request
from flask_restful import abort
from marshmallow import fields, Schema

from github_interface.interfaces.web_server_github_interface import WebServerGithubInterface
from mongo.constants.model_fields import ModelFields
from utils.code_formatter import CodeFormatter
from web_server.endpoints.abstract_endpoint import AbstractEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountFSNodeEndpoint(AbstractAccountEndpoint):

    def __init__(self):
        super().__init__()
        self._get_output_schema_instance = Schema.from_dict({
            ModelFields.TYPE: fields.Str(required=True),
            ModelFields.CONTENT: fields.Str(required=False),
            ModelFields.SUB_FS_NODES: fields.Nested(Schema.from_dict({
                ModelFields.NAME: fields.Str(required=True)
            }), required=False, many=True)
        })()

    def get(self, github_account_login):

        # Get the repository
        repo_name = request.args[ModelFields.REPO_NAME]
        # Get the content at path
        path = request.args[ModelFields.PATH] if request.args[ModelFields.PATH] else ""

        if not repo_name:
            return abort(400, message="A repo should be specified")

        repo_interface = WebServerGithubInterface(
            session[AbstractEndpoint.COOKIE_USER_LOGIN_FIELD]
        ).request_repo(github_account_login, repo_name)

        # TODO: fix this so we don't have to deepcopy
        fs_node = repo_interface.get_fs_node_at_path(path)

        # Syntax highlighting for file
        if fs_node.type == 'file':
            fs_node.content = CodeFormatter().format(path, fs_node.content)

        # Return the response
        # TODO: return only the necessary fields, not the entire repo object
        return self._create_validated_response(fs_node)
