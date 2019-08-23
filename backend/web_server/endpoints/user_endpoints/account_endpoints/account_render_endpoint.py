from flask import request, session

from github_interface.interfaces.authenticated_github_interface import AuthenticatedGithubInterface
from mongo.collection_clients.clients.db_document_client import DbDocumentClient
from mongo.constants.model_fields import ModelFields
from utils.code_formatter import CodeFormatter
from web_server.endpoints.abstract_endpoint import AbstractEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountRenderEndpoint(AbstractAccountEndpoint):

    def get(self, github_account_login):

        name = request.args[ModelFields.REPO_NAME]

        # Get the documentation doc
        doc = DbDocumentClient().find_one(github_account_login, name)

        refs = []
        for ref in doc.refs:
            repo_interface = AuthenticatedGithubInterface(session[AbstractEndpoint.USER_LOGIN_FIELD])\
                .request_repo(ref.github_account_login,ref.repo_name)

            lines_from_file_content = repo_interface.get_fs_node_at_path(ref.path).content.splitlines()[
                                      ref.start_line - 1: ref.end_line]

            content = '\n'.join(lines_from_file_content)
            formatted_code = CodeFormatter().format(ref.path, content, ref.start_line)

            # TODO: create a function on object sent to the frontend to populate all the non sensitive information that it
            #  contains (to send to the frontend) so that we don't do it manually
            ref_json = ref.to_json()
            ref_json['code'] = formatted_code
            refs.append(ref_json)

        return self._create_response({
            'name': name,
            'content': doc.content,
            'refs': refs
        })
