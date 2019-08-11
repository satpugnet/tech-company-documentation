from github import Github

from github_interface.github_types.github_repository import GithubRepository
from mongo.models.account_installation import AccountInstallation


class NonAuthenticatedGithubInterface:

    __repo_cache = {}

    # TODO: use repo id and not repo name for the cache
    @staticmethod
    def get_repo(installation_account_login, repo_name):
        print("Retrieving single repo")
        installation_token = AccountInstallation.find(installation_account_login).installation_token
        return NonAuthenticatedGithubInterface.__get_repo_helper(installation_token, repo_name)

    @staticmethod
    def __get_repo_helper(installation_token, repo_name):
        github_account = Github(installation_token)

        if repo_name not in NonAuthenticatedGithubInterface.__repo_cache:
            NonAuthenticatedGithubInterface.__repo_cache[repo_name] = GithubRepository(github_account.get_repo(repo_name))

        return NonAuthenticatedGithubInterface.__repo_cache[repo_name]

    @staticmethod
    def get_repos(installation_account_login):
        print("Retrieving repos")
        # TODO: check if user_login is required in the parameters
        installation_token = AccountInstallation.find(installation_account_login).installation_token
        github_account = Github(installation_token)
        repos = []

        # raw_repos = github_account.get_user().get_repos() <-- This is the call using the user token instead of the installation token
        raw_installation_repos = github_account.get_installation(-1).get_repos()

        for installation_repo in raw_installation_repos:
            repos.append(GithubRepository(installation_repo))
        return repos

    @staticmethod
    def get_user_login(user_access_token):
        print("Retrieving user login")
        github_account = Github(user_access_token)

        user = github_account.get_user()
        return user.login




