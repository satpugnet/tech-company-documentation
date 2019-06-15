from github import Github

from github_interface.github_types.github_repository import GithubRepository


class GithubInterface:

    def __init__(self, access_token):
        self.__github_account = Github(access_token)

    def get_repo(self, repo_name):
        return GithubRepository(self.__github_account.get_repo(repo_name))

    def get_repos(self):
        repos = []
        for repo in self.__github_account.get_user().get_repos():
            repos.append(GithubRepository(repo))
        return repos

    def get_repo_names(self):
        return [r.get_full_name() for r in self.get_repos()]

