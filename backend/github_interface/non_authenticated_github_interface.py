from flask import logging
from github import Github

from github_interface.github_types.github_repository import GithubRepository
from mongo.models.db_account_installation import DbAccountInstallation

class NonAuthenticatedGithubInterface:

    __repo_cache = {}

    # TODO: the repo_full_name contains the org_user_account in it so the org_user_account should be removed
    @staticmethod
    def get_repo(org_user_account, repo_full_name):
        print("Retrieving single repo " + str(repo_full_name))
        installation_token = DbAccountInstallation.find(org_user_account).installation_token
        return NonAuthenticatedGithubInterface.__get_repo_helper(installation_token, repo_full_name)

    @staticmethod
    def __get_repo_helper(installation_token, repo_full_name):
        github_account = Github(installation_token)

        if repo_full_name not in NonAuthenticatedGithubInterface.__repo_cache:
            NonAuthenticatedGithubInterface.__repo_cache[repo_full_name] = GithubRepository(github_account.get_repo(repo_full_name))

        return NonAuthenticatedGithubInterface.__repo_cache[repo_full_name]

    @staticmethod
    def get_repos(org_user_account):
        print("Retrieving repos for " + str(org_user_account))
        # TODO: check if user_login is required in the parameters
        installation_token = DbAccountInstallation.find(org_user_account).installation_token
        github_account = Github(installation_token)
        repos = []

        raw_installation_repos = github_account.get_installation(-1).get_repos()

        for installation_repo in raw_installation_repos:
            repos.append(GithubRepository(installation_repo))
        return repos

    @staticmethod
    def get_user_login(user_token):
        print("Retrieving user login")
        github_account = Github(user_token)

        user = github_account.get_user()
        return user.login




