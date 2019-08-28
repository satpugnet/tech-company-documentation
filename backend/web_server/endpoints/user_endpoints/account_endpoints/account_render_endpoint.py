from flask import request
from marshmallow import Schema, fields

from mongo.collection_clients.clients.db_doc_client import DbDocClient
from mongo.collection_clients.clients.db_github_fs_node_client import DbGithubFSNodeClient
from mongo.constants.model_fields import ModelFields
from utils.code_formatter import CodeFormatter
from utils.path_manipulator import PathManipulator
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountRenderEndpoint(AbstractAccountEndpoint):
    """
    Endpoint for handling the rendering of the doc.
    """

    def __init__(self):
        super().__init__()
        self._get_output_schema_instance = Schema.from_dict({
            ModelFields.CONTENT: fields.Str(required=True),
            ModelFields.REFS: fields.Nested(Schema.from_dict({
                ModelFields.ID: fields.Str(required=True),
                ModelFields.CODE: fields.Str(required=True)
            }), required=True, many=True)
        })()

    def get(self, github_account_login):

        doc_name = request.args[ModelFields.DOC_NAME]

        # Get the documentation doc
        doc = DbDocClient().find_one(github_account_login, doc_name)

        refs = []
        for ref in doc.refs:

            github_fs_node = DbGithubFSNodeClient().find_one(ref.github_account_login, ref.repo_name, ref.path)

            code = CodeFormatter().format(ref.path, github_fs_node.content, ref.start_line, ref.end_line)

            ref_json = ref.to_json()
            ref_json[ModelFields.CODE] = code
            refs.append(ref_json)

        return self._create_validated_response({
            ModelFields.CONTENT: doc.content,
            ModelFields.REFS: refs
        })
