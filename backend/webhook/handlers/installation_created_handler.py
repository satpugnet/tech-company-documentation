from github_interface.constants.github_api_fields import GithubApiFields
from github_interface.interfaces.github_authorisation_interface import GithubAuthorisationInterface
from github_interface.interfaces.webhook_github_interface import WebhookGithubInterface
from mongo.collection_clients.clients.db_github_file_client import DbGithubFileClient
from mongo.collection_clients.clients.db_github_installation_client import DbGithubInstallationClient
from mongo.collection_clients.clients.db_repo_client import DbRepoClient
from tools import logger
from tools.file_system_interface import FileSystemInterface
from webhook.handlers.abstract_request_handler import AbstractRequestHandler


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
        self.__insert_db_github_files()

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
            DbRepoClient().upsert_one(
                self.__github_account_login,
                repo_name
            )

    def __insert_db_github_files(self):
        """
        Insert all of the repos github files in the database for quicker access in the future.
        We are mirroring the github repo state in our db.
        """
        logger.get_logger().info("Inserting and mirroring all the github files in repo %s in the database", self.__github_account_login)

        for repo_name in self.__repos_name:
            installation_repo = WebhookGithubInterface(self.__github_account_login).request_repo(repo_name)
            flat_files = installation_repo.get_all_files_flat()

            for file in flat_files:
                DbGithubFileClient().insert_one(
                    self.__github_account_login,
                    repo_name,
                    file.dir_path,
                    file.name,
                    file.type,
                    file.content
                )
