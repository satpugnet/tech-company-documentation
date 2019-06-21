from github import Github

from github_interface.github_types.github_repository import GithubRepository


class GithubInterface:

    def __init__(self, access_token):
        self.__github_account = Github(access_token)
        self.__repo_cache = {}

    def get_repo(self, repo_name):
        if repo_name in self.__repo_cache:
            repo = self.__repo_cache[repo_name]
        else:
            self.__repo_cache[repo_name] = GithubRepository(self.__github_account.get_repo(repo_name))
            repo = self.__repo_cache[repo_name]
        return repo

    def get_repos(self):
        repos = []
        for repo in self.__github_account.get_user().get_repos():
            repos.append(GithubRepository(repo))
        return repos

