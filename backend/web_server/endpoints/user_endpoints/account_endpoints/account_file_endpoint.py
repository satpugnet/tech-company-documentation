from flask import session, request
from flask_restful import abort

from github_interface.interfaces.authenticated_github_interface import AuthenticatedGithubInterface
from mongo.constants.db_fields import ModelFields
from utils.code_formatter import CodeFormatter
from web_server.endpoints.abstract_endpoint import AbstractEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountFileEndpoint(AbstractAccountEndpoint):

    def get(self, github_account_login):

        # Get the repository
        repo_name = request.args[ModelFields.REPO_NAME]

        if not repo_name:
            return abort(400, message="A repo should be specified")

        repo_interface = AuthenticatedGithubInterface(
            session[AbstractEndpoint.USER_LOGIN_FIELD]
        ).request_repo(github_account_login, repo_name)

        # Get the content at path
        path = request.args[ModelFields.PATH] if request.args[ModelFields.PATH] else ""

        # TODO: fix this so we don't have to deepcopy
        fs_node = repo_interface.get_fs_node_at_path(path)

        # Syntax highlighting for file
        if fs_node.type == 'file':
            fs_node.content = CodeFormatter().format(path, fs_node.content)

        # Return the response
        # TODO: return only the necessary fields, not the entire repo object
        return self._create_response(fs_node)
