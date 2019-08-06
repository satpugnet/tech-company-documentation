import requests
from github import Github

from github_interface.github_types.github_repository import GithubRepository
from mongo.models.installation import Installation
from mongo.models.user import User
from abc import ABC, abstractmethod


class AbstractGithubInterface(ABC):

    __repo_cache = {}

    # TODO: use repo id and not repo name for the cache
    @staticmethod
    @abstractmethod
    def get_repo(user_login, installation_account_login, repo_name):
        installation_token = Installation.find(installation_account_login).installation_token
        return AbstractGithubInterface.__get_repo_helper(installation_token, repo_name)

    @staticmethod
    @abstractmethod
    def get_repo_without_user_authentification(installation_account_login, repo_name):
        installation_token = Installation.find(installation_account_login).installation_token
        return AbstractGithubInterface.__get_repo_helper(installation_token, repo_name)

    @staticmethod
    def __get_repo_helper(installation_token, repo_name):
        github_account = Github(installation_token)

        if repo_name in AbstractGithubInterface.__repo_cache:
            repo = AbstractGithubInterface.__repo_cache[repo_name]
        else:
            AbstractGithubInterface.__repo_cache[repo_name] = GithubRepository(github_account.get_repo(repo_name))
            repo = AbstractGithubInterface.__repo_cache[repo_name]
        return repo

    @staticmethod
    @abstractmethod
    def get_repos(user_login, installation_account_login):
        # TODO: check if user_login is required in the parameters
        installation_token = Installation.find(installation_account_login).installation_token
        github_account = Github(installation_token)
        repos = []

        # raw_repos = github_account.get_user().get_repos() <-- This is the call using the user token instead of the installation token
        raw_installation_repos = github_account.get_installation(-1).get_repos()

        for installation_repo in raw_installation_repos:
            repos.append(GithubRepository(installation_repo))
        return repos

    @staticmethod
    def get_user_login(user_access_token):
        github_account = Github(user_access_token)

        user = github_account.get_user()
        return user.login

    @staticmethod
    @abstractmethod
    def get_user_installations(user_login):
        user_access_token = User.find(user_login).user_token
        response = requests.get(url="https://api.github.com/user/installations",
                                headers={
                                    "Authorization": "token " + user_access_token,
                                    "Accept": "application/vnd.github.machine-man-preview+json"
                                })
        return response.json()


