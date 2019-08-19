from github import Github

from github_interface.interfaces.repo_github_interface import RepoGithubInterface
from mongo.collection_clients.db_github_installation_client import DbGithubInstallationClient
from tools import logger


class NonAuthenticatedGithubInterface:
    def __init__(self, github_account_login):
        installation_token = DbGithubInstallationClient().find_one(github_account_login).installation_token
        self.__github_account_login = github_account_login
        self.__installation_github_account = Github(installation_token)

    def request_repo(self, repo_name):
        logger.get_logger().info("Requesting a single repo: %s/%s", self.__github_account_login, str(repo_name))

        repo_full_name = str(self.__github_account_login) + "/" + str(repo_name)

        return RepoGithubInterface(self.__installation_github_account.get_repo(repo_full_name))

    def request_repos(self):
        logger.get_logger().info("Requesting repos for %s", self.__github_account_login)

        raw_installation_repos = self.__installation_github_account.get_installation(-1).get_repos()

        return [RepoGithubInterface(raw_installation_repo) for raw_installation_repo in raw_installation_repos]
