from github_interface.constants.github_api_fields import GithubApiFields
from github_interface.interfaces.github_authorisation_interface import GithubAuthorisationInterface
from mongo.collection_clients.clients.db_github_installation_client import DbGithubInstallationClient
from mongo.collection_clients.clients.db_repo_client import DbRepoClient
from tools import logger
from tools.file_system_interface import FileSystemInterface
from webhook.handlers.abstract_request_handler import AbstractRequestHandler
from webhook.handlers.actions.mirror_github_files_to_db import MirrorGithubFilesToDb


class InstallationCreatedHandler(AbstractRequestHandler):
    """
    A handler for installation created event.
    """

    def __init__(self, data):
        super().__init__()
        self.__github_account_login = data[GithubApiFields.INSTALLATION][GithubApiFields.ACCOUNT][GithubApiFields.LOGIN]
        self.__repos_name = [data_repo[GithubApiFields.NAME] for data_repo in data[GithubApiFields.REPOSITORIES]]
        self.__installation_id = data[GithubApiFields.INSTALLATION][GithubApiFields.ID]

    def enact(self):
        logger.get_logger().info("Handling th installation created event for %s with repositories %s and installation id %s",
                                 self.__github_account_login, str(self.__repos_name), str(self.__installation_id))

        self.__insert_db_installation_token()
        self.__insert_db_repos()
        MirrorGithubFilesToDb(self.__repos_name, self.__github_account_login).perform()

    def __insert_db_installation_token(self):
        """
        Insert the installation token in the databse.
        """
        logger.get_logger().info("Inserting the installation token for %s in the database", self.__github_account_login)

        installation_token, expires_at = GithubAuthorisationInterface.request_installation_token(
            self.__installation_id,
            FileSystemInterface.load_private_key()
        )

        DbGithubInstallationClient().insert_one(
            self.__github_account_login,
            self.__installation_id,
            installation_token,
            expires_at
        )

    def __insert_db_repos(self):
        """
        Insert the repos from the installation in the database.
        """
        logger.get_logger().info("Inserting the repos from the installation %s in the database", self.__github_account_login)

        for repo_name in self.__repos_name:
            DbRepoClient().insert_one(
                self.__github_account_login,
                repo_name
            )

