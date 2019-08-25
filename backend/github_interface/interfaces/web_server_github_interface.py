import multiprocessing as mp

import requests
from github import Github, UnknownObjectException

from github_interface.constants.github_api_fields import GithubApiFields
from github_interface.constants.github_api_values import GithubApiValues
from github_interface.interfaces.helper_interfaces.repo_github_interface import RepoGithubInterface
from github_interface.interfaces.webhook_github_interface import WebhookGithubInterface
from github_interface.wrappers.models.github_installation_model import GithubInstallationModel
from mongo.collection_clients.clients.db_user_client import DbUserClient
from tools import logger


class WebServerGithubInterface:
    """
    This is an interface for accessing github using at the same time the user token and the installation token. This
    ensures that the Github app is not accessing repos that either the user has no access to (but could be accessed with
    the installation token) or that the user did not allow the Github app to access (but could be accessed with the user
    token. In order to ensure that none of this is breached, we will return the common repos returned by both of those
    calls.
    """

    def __init__(self, user_login):
        self.__user_login = user_login
        self.__user_github_account = Github(DbUserClient().find_one(self.__user_login).token)

    def request_repo(self, github_account_login, repo_name):
        """
        :return: Returns a single repo (an interface) which the user and the Github app are allowed to access.
        """
        logger.get_logger().warning("Getting repository %s/%s for user %s, filtered using user token and installation token", github_account_login, repo_name, self.__user_login)

        installation_authorised_repo_interface = WebhookGithubInterface(github_account_login).request_repo(repo_name)
        user_authorised_repo_interface = self.__get_user_authorised_repo(installation_authorised_repo_interface.repo.full_name)

        return self.__get_repo_in_common(installation_authorised_repo_interface, user_authorised_repo_interface)

    def request_repos(self, github_account_login):
        """
        :return: Returns all repos (as a list of interfaces) under this account and accessible by the user.
        """
        logger.get_logger().warning("Getting all repositories for account %s for user %s, filtered using user token and installation token", github_account_login, self.__user_login)

        installation_authorised_repos_interface = WebhookGithubInterface(github_account_login).request_repos()
        user_authorised_repos_interface = []

        if len(installation_authorised_repos_interface) > 0:
            user_authorised_repos_interface = self.__get_user_authorised_repos(
                installation_authorised_repos_interface,
                github_account_login,
                installation_authorised_repos_interface[0].repo.owner_type
            )

        return self.__get_repos_in_common(
            installation_authorised_repos_interface,
            user_authorised_repos_interface
        )

    def request_installations(self):
        """
        :return: A list of Github app installations which the user has access to.
        """
        logger.get_logger().info("Requesting user installations for %s", self.__user_login)

        user_token = DbUserClient().find_one(self.__user_login).token

        response = requests.get(url="https://api.github.com/user/installations",
                                headers={
                                    "Authorization": "token " + user_token,
                                    "Accept": "application/vnd.github.machine-man-preview+json"
                                })

        filtered_user_installations = self.__filter_user_installations(response.json()[GithubApiFields.INSTALLATIONS])

        return [
            GithubInstallationModel(installation[GithubApiFields.ID], installation[GithubApiFields.ACCOUNT][GithubApiFields.LOGIN])
            for installation in filtered_user_installations
        ]

    def __get_user_authorised_repo(self, repo_full_name):
        """
        :return: A single repo (interface) if the user has access to it.
        """

        try:
            raw_user_authorised_repo = self.__user_github_account.get_repo(repo_full_name)
            return RepoGithubInterface(raw_user_authorised_repo)

        except UnknownObjectException:
            logger.get_logger().info("The user %s is not authorised to access the repo %s", str(self.__user_login), repo_full_name)
            return None

    def __get_user_authorised_repos(self, installation_authorised_repos, github_account_login, account_type):
        """
        :param installation_authorised_repos: A list of repo that the installation has access to.
        :param github_account_login: The account for which the repos are requested.
        :param account_type: the type of the Github account.
        :return: A list of all repos (interfaces) that the user can access.
        """

        raw_private_repos = []

        if account_type == GithubApiValues.ORGANISATION:
            raw_github_account_repos = list(self.__user_github_account.get_organization(github_account_login).get_repos())

        elif github_account_login == self.__user_login:
            raw_github_account_repos = list(self.__user_github_account.get_user().get_repos())

        else:
            installation_private_repos = list(filter(lambda repo_interface: repo_interface.repo.private, installation_authorised_repos))
            raw_github_account_repos = list(self.__user_github_account.get_user(github_account_login).get_repos())
            raw_private_repos = self.__get_user_repos_in_parallel(installation_private_repos)

        authorised_repos = [RepoGithubInterface(raw_repo) for raw_repo in raw_github_account_repos] + raw_private_repos
        return sorted(authorised_repos, key=lambda repo_interface: repo_interface.repo.name)

    def __get_user_repos_in_parallel(self, repos):
        """
        Fetch all the given repos in parallel using the user token.
        """

        pool = mp.Pool()

        repos_full_name = [repo.full_name for repo in repos]
        raw_repos = list(filter(None, pool.map(self.__get_user_authorised_repo, repos_full_name)))

        pool.close()

        return raw_repos

    def __filter_user_installations(self, raw_user_installations):
        """
        Select all installation that the user is allowed to access. Currently, we only allow to access organisation and
        its own personal account.
        """

        returned_user_installations = []

        for raw_user_installation in raw_user_installations:

            if self.__is_current_user_account(raw_user_installation) or self.__is_organisation(raw_user_installation):
                returned_user_installations.append(raw_user_installation)

            else:
                logger.get_logger().info("The installation %s has been filtered out for the user %s",
                                         raw_user_installation[GithubApiFields.ACCOUNT][GithubApiFields.LOGIN], self.__user_login)

        return returned_user_installations

    def __get_repo_in_common(self, repo_interfaces1, repo_interfaces2):
        repo_interfaces = self.__get_repos_in_common(
            [repo_interfaces1],
            [repo_interfaces2]
        )

        return repo_interfaces[0] if len(repo_interfaces) == 1 else None

    def __get_repos_in_common(self, repo_interfaces1, repo_interfaces2):
        repos1_full_names = [repo_interface.repo.full_name for repo_interface in repo_interfaces2]

        return list(filter(lambda repo_interface: repo_interface.repo.full_name in repos1_full_names, repo_interfaces1))

    def __is_current_user_account(self, raw_user_installation):
        return raw_user_installation[GithubApiFields.ACCOUNT][GithubApiFields.TYPE] == GithubApiValues.USER \
               and raw_user_installation[GithubApiFields.ACCOUNT][GithubApiFields.LOGIN] == self.__user_login

    def __is_organisation(self, raw_user_installation):
        return raw_user_installation[GithubApiFields.ACCOUNT][GithubApiFields.TYPE] == GithubApiValues.ORGANISATION

