import uuid

from flask import request
from marshmallow import Schema, fields

from mongo.collection_clients.clients.db_github_fs_node_client import DbGithubFSNodeClient
from mongo.constants.model_fields import ModelFields
from utils.code_formatter import CodeFormatter
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

        github_fs_node = DbGithubFSNodeClient().find_one(github_account_login, repo_name, path)

        code = CodeFormatter().format(path, github_fs_node.content, start_line, end_line)

        return self._create_validated_response({
            ModelFields.ID: str(uuid.uuid1()),  # generate a unique id for the reference
            ModelFields.CODE: code
        })
