from datetime import datetime, timezone

from github import Github

from github_interface.interfaces.github_authorisation_interface import GithubAuthorisationInterface
from github_interface.interfaces.helper_interfaces.repo_github_interface import RepoGithubInterface
from mongo.collection_clients.clients.db_github_installation_client import DbGithubInstallationClient
from tools import logger
from tools.file_system_interface import FileSystemInterface


class WebhookGithubInterface:
    """
    NEVER USE IN WEB SERVER.

    An interface for accessing github that should only be used by the webhook as it authenticate using the installation
    token (server to server) and not using a user token (user to server). Therefore, it has unrestricted access to
    anything our app has access to and should never be used in the web server.
    """

    def __init__(self, github_account_login):
        installation_token = self.__request_cached_installation_token(github_account_login)
        self.__github_account_login = github_account_login
        self.__installation_github_account = Github(installation_token)

    def request_repo(self, repo_name):
        """
        Fetch a single repo from github and returns an interface for accessing information about this repo.
        """
        logger.get_logger().info("Requesting a single repo: %s/%s", str(self.__github_account_login), str(repo_name))

        repo_full_name = str(self.__github_account_login) + "/" + str(repo_name)

        return RepoGithubInterface(self.__installation_github_account.get_repo(repo_full_name))

    def request_repos(self):
        """
        Fetch all repos from github under this installation and returns a list of interfaces to access them.
        """
        logger.get_logger().info("Requesting repos for %s", self.__github_account_login)

        raw_installation_repos = self.__installation_github_account.get_installation(-1).get_repos()

        return [RepoGithubInterface(raw_installation_repo) for raw_installation_repo in raw_installation_repos]

    def __request_cached_installation_token(self, github_account_login):
        """
        Retrieved the access token stored in the database if not expired, otherwise, request a new one from github and
        add it to the db.
        """

        cached_installation = DbGithubInstallationClient().find_one(github_account_login)

        if cached_installation.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            installation_token, expires_at = GithubAuthorisationInterface.request_installation_token(cached_installation.id, FileSystemInterface.load_private_key())
            DbGithubInstallationClient().update_one_token(cached_installation.mongo_id, installation_token, expires_at)

            return installation_token

        return cached_installation.token
