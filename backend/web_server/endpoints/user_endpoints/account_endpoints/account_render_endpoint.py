from flask import request, session
from marshmallow import Schema, fields

from github_interface.interfaces.web_server_github_interface import WebServerGithubInterface
from mongo.collection_clients.clients.db_doc_client import DbDocClient
from mongo.constants.model_fields import ModelFields
from utils.code_formatter import CodeFormatter
from web_server.endpoints.abstract_endpoint import AbstractEndpoint
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
            repo_interface = WebServerGithubInterface(session[AbstractEndpoint.COOKIE_USER_LOGIN_FIELD])\
                .request_repo(ref.github_account_login,ref.repo_name)

            lines_from_file_content = repo_interface.get_fs_node_at_path(ref.path).content.splitlines()[
                                      ref.start_line - 1: ref.end_line]

            content = '\n'.join(lines_from_file_content)
            formatted_code = CodeFormatter().format(ref.path, content, ref.start_line)

            # TODO: create a function on object sent to the frontend to populate all the non sensitive information that it
            #  contains (to send to the frontend) so that we don't do it manually
            ref_json = ref.to_json()
            ref_json[ModelFields.CODE] = formatted_code
            refs.append(ref_json)  # only id and code are used

        return self._create_validated_response({
            ModelFields.CONTENT: doc.content,
            ModelFields.REFS: refs
        })
