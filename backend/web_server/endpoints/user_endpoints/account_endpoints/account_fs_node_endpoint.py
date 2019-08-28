from flask import request
from flask_restful import abort
from marshmallow import fields, Schema

from mongo.collection_clients.clients.db_github_fs_node_client import DbGithubFSNodeClient
from mongo.constants.model_fields import ModelFields
from tools import logger
from utils.code_formatter import CodeFormatter
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


# TODO: currently the authorisation to access a specific repo in an organisation is not checked, by default, if a user
#  has access to an installation, it has access to all repos
class AccountFSNodeEndpoint(AbstractAccountEndpoint):
    """
    Endpoint for handling the github file system node.
    """

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
            logger.get_logger().error("The repo name has not been specified.")
            return abort(400, message="A repo should be specified")

        github_fs_node = DbGithubFSNodeClient().find_one(github_account_login, repo_name, path)

        # TODO: This if statement is due to the fact that it is not possible to assign a value of the Schema to several
        #  fields types, maybe creating 2 different schema would be a good idea and returning only content in both cases
        github_fs_node_json = github_fs_node.to_json()
        if github_fs_node.type == 'file':
            github_fs_node_json[ModelFields.CONTENT] = CodeFormatter().format(path, github_fs_node.content)  # Syntax highlighting for file

        else:
            github_fs_node_json[ModelFields.SUB_FS_NODES] = [
                {ModelFields.NAME: fs_node} for fs_node in github_fs_node_json[ModelFields.CONTENT]
            ]
            github_fs_node_json[ModelFields.CONTENT] = None

        # Return the response
        return self._create_validated_response(github_fs_node_json)
