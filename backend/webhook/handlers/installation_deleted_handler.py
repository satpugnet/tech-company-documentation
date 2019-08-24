from github_interface.constants.github_api_fields import GithubApiFields
from mongo.collection_clients.clients.db_github_file_client import DbGithubFileClient
from mongo.collection_clients.clients.db_github_installation_client import DbGithubInstallationClient
from mongo.collection_clients.clients.db_repo_client import DbRepoClient
from webhook.handlers.abstract_request_handler import AbstractRequestHandler


class InstallationDeletedHandler(AbstractRequestHandler):

    def __init__(self, data):
        super().__init__()
        self.__github_account_login = data[GithubApiFields.INSTALLATION][GithubApiFields.ACCOUNT][GithubApiFields.LOGIN]

    # TODO: add a flag in documents reference stating when an installation has been deleted and therefore no access to the ref
    def enact(self):
        self.__clear_db_github_installation()
        self.__clear_db_repo()
        self.__clear_db_github_file()

    def __clear_db_github_installation(self):
        DbGithubInstallationClient().remove(
            self.__github_account_login
        )

    def __clear_db_repo(self):
        DbRepoClient().remove(
            self.__github_account_login
        )

    def __clear_db_github_file(self):
        DbGithubFileClient().remove(
            self.__github_account_login
        )
