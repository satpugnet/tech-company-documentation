import multiprocessing as mp

import requests
from github import Github, UnknownObjectException

from github_interface.github_types.github_installation import GithubInstallation
from github_interface.github_types.github_repository import GithubRepository
from github_interface.non_authenticated_github_interface import NonAuthenticatedGithubInterface
from mongo.models.user import User


class AuthenticatedGithubInterface:

    __installation_cache = {}

    def __init__(self, user_login):
        self.__user_login = user_login
        self.__user_github_object = self.__initialise_user_github_object()

    def get_repo(self, installation_account_login, repo_name):
        installation_authorised_repo = NonAuthenticatedGithubInterface.get_repo(installation_account_login, repo_name)
        user_authorised_repo = self._get_user_authorised_repo(installation_authorised_repo.full_name)
        return self.__get_common_repo(installation_authorised_repo, user_authorised_repo)

    def get_repos(self, installation_account_login):
        installation_authorised_repos = NonAuthenticatedGithubInterface.get_repos(installation_account_login)
        user_authorised_repos = self.__get_user_authorised_repos(installation_authorised_repos, installation_account_login,
                                                                 installation_authorised_repos[0].owner["type"]) if len(installation_authorised_repos) > 0 else []
        return self.__get_common_repos(installation_authorised_repos, user_authorised_repos)

    def get_user_installations(self):
        print("Retrieving user installation " + str(self.__user_login))
        if self.__user_login not in AuthenticatedGithubInterface.__installation_cache:
            user_access_token = User.find(self.__user_login).user_token
            response = requests.get(url="https://api.github.com/user/installations",
                                    headers={
                                        "Authorization": "token " + user_access_token,
                                        "Accept": "application/vnd.github.machine-man-preview+json"
                                    })
            user_installations = [GithubInstallation(installation) for installation in self.__filter_user_installations(response.json()["installations"])]
            AuthenticatedGithubInterface.__installation_cache[self.__user_login] = user_installations

        return AuthenticatedGithubInterface.__installation_cache[self.__user_login]

    def _get_user_authorised_repo(self, repo_full_name):
        try:
            user_authorised_repo = self.__user_github_object.get_repo(repo_full_name)
            return GithubRepository(user_authorised_repo)
        except UnknownObjectException:
            print("The user " + str(self.__user_login) + " is not authorised to access the repo " + str(repo_full_name))
            return None

    def __get_user_authorised_repos(self, installation_authorised_repos, installation_account_login, account_type):
        private_repos = list(filter(lambda repo: repo.private, installation_authorised_repos))
        raw_private_repos = []

        if account_type == "Organization":
            raw_installation_repos = list(self.__user_github_object.get_organization(installation_account_login).get_repos())
        elif installation_account_login == self.__user_login:
            raw_installation_repos = list(self.__user_github_object.get_user().get_repos())
        else:
            raw_installation_repos = list(self.__user_github_object.get_user(installation_account_login).get_repos())
            pool = mp.Pool()
            raw_private_repos = list(filter(None, pool.map(self._get_user_authorised_repo, [repo.full_name for repo in private_repos])))
            pool.close()

        authorised_repos = [GithubRepository(repo) for repo in raw_installation_repos] + raw_private_repos
        return sorted(authorised_repos, key=lambda repo: repo.full_name)

    def __get_common_repo(self, repo1, repo2):
        repos = self.__get_common_repos([repo1], [repo2])

        return repos[0] if len(repos) == 1 else None

    def __get_common_repos(self, repos1, repos2):
        repos1_full_name = [repo.full_name for repo in repos2]

        return list(filter(lambda repo: repo.full_name in repos1_full_name, repos1))

    def __filter_user_installations(self, user_installations):
        returned_user_installations = []
        for user_installation in user_installations:
            if user_installation["account"]["type"] == "User" and user_installation["account"]["login"] == self.__user_login:
                returned_user_installations.append(user_installation)
            elif user_installation["account"]["type"] == "Organization":
                returned_user_installations.append(user_installation)
            else:
                print("The installation " + str(user_installation["account"]["login"]) + " has been filtered out for the user " + str(self.__user_login))
        return returned_user_installations

    def __initialise_user_github_object(self):
        user_token = User.find(self.__user_login).user_token
        return Github(user_token)
