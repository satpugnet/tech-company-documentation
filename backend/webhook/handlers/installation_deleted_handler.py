from github_interface.constants.github_api_fields import GithubApiFields
from mongo.collection_clients.clients.db_github_file_client import DbGithubFileClient
from mongo.collection_clients.clients.db_github_installation_client import DbGithubInstallationClient
from mongo.collection_clients.clients.db_repo_client import DbRepoClient
from tools import logger
from webhook.handlers.abstract_request_handler import AbstractRequestHandler


class InstallationDeletedHandler(AbstractRequestHandler):
    """
    A handler for installation deleted event.
    """

    def __init__(self, data):
        super().__init__()
        self.__github_account_login = data[GithubApiFields.INSTALLATION][GithubApiFields.ACCOUNT][GithubApiFields.LOGIN]

    # TODO: add a flag in documents reference stating when an installation has been deleted and therefore
    #  user should not have access to the ref
    def enact(self):
        logger.get_logger().info("Handling the installation deleted event for %s", self.__github_account_login)

        self.__clear_db_github_installation()
        self.__clear_db_repo()
        self.__clear_db_github_file()

    def __clear_db_github_installation(self):
        """
        Clear the github installation fron the database.
        """
        logger.get_logger().info("Clearing the github installation collection for %s", self.__github_account_login)

        DbGithubInstallationClient().remove(
            self.__github_account_login
        )

    def __clear_db_repo(self):
        """
        Clear the repo from the database.
        """
        logger.get_logger().info("Clearing the repo collection for %s", self.__github_account_login)

        DbRepoClient().remove(
            self.__github_account_login
        )

    def __clear_db_github_file(self):
        """
        Clear all of the github repos cached file from the database.
        """
        logger.get_logger().info("Clearing the github repos cached file collection for %s", self.__github_account_login)

        DbGithubFileClient().remove(
            self.__github_account_login
        )
