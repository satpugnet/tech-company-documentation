import uuid

from flask import request, session

from github_interface.interfaces.authenticated_github_interface import AuthenticatedGithubInterface
from mongo.constants.model_fields import ModelFields
from utils.code_formatter import CodeFormatter
from web_server.endpoints.abstract_endpoint import AbstractEndpoint
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountLinesEndpoint(AbstractAccountEndpoint):

    def get(self, github_account_login):

        repo_name = request.args[ModelFields.REPO_NAME]
        path = request.args[ModelFields.PATH]
        start_line = int(request.args[ModelFields.START_LINE])
        end_line = int(request.args[ModelFields.END_LINE])

        repo_interface = AuthenticatedGithubInterface(session[AbstractEndpoint.USER_LOGIN_FIELD]).request_repo(github_account_login, repo_name)

        fs_node = repo_interface.get_fs_node_at_path(path)
        content = ''.join(fs_node.content.splitlines(keepends=True)[start_line - 1: end_line])

        code = CodeFormatter().format(path, content, start_line)

        return self._create_response({
            'id': str(uuid.uuid1()),  # generate a unique id for the reference
            'code': code,
            'github_account_login': github_account_login,
            'repo_name': repo_name,
            'path': path,
            'start_line': start_line,
            'end_line': end_line,
        })
