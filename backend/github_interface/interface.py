import hmac
from hashlib import sha1

import requests
from github import Github, GithubIntegration

from github_interface.github_types.github_repository import GithubRepository
from mongo.models.user import User
from utils.constants import GITHUB_APP_IDENTIFIER


class GithubInterface:

    __repo_cache = {}

    # TODO: use repo id and not repo name for the cache
    @staticmethod
    def get_repo(user_login, installation_account_login, repo_name):
        installation_token = User.find_installation(user_login, installation_account_login).installation_token
        return GithubInterface.__get_repo_helper(installation_token, repo_name)

    @staticmethod
    def get_repo_without_user_authentification(installation_account_login, repo_name):
        installation_token = User.find_installation_without_user_authentification(installation_account_login).installation_token
        return GithubInterface.__get_repo_helper(installation_token, repo_name)

    @staticmethod
    def __get_repo_helper(installation_token, repo_name):
        github_account = Github(installation_token)

        if repo_name in GithubInterface.__repo_cache:
            repo = GithubInterface.__repo_cache[repo_name]
        else:
            GithubInterface.__repo_cache[repo_name] = GithubRepository(github_account.get_repo(repo_name))
            repo = GithubInterface.__repo_cache[repo_name]
        return repo

    @staticmethod
    def get_repos(user_login, installation_account_login):
        installation_token = User.find_installation(user_login, installation_account_login).installation_token
        github_account = Github(installation_token)
        repos = []

        # raw_repos = github_account.get_user().get_repos() <-- This is the call using the user token instead of the installation token
        raw_repos = github_account.get_installation(-1).get_repos()

        for repo in raw_repos:
            repos.append(GithubRepository(repo))
        return repos

    @staticmethod
    def get_user_access_token(client_id, client_secret, code, redirect_uri):
        params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri
        }
        r = requests.get(url="https://github.com/login/oauth/access_token", params=params)
        content = r.content.decode("utf-8")
        user_access_token = content[content.find("access_token=") + 13: content.find("&")]

        return user_access_token

    @staticmethod
    def get_user_login(user_access_token):
        github_account = Github(user_access_token)

        user = github_account.get_user()
        return user.login

    @staticmethod
    def get_user_installations(user_login):
        user_access_token = User.find(user_login).user_token
        response = requests.get(url="https://api.github.com/user/installations",
                                headers={
                                    "Authorization": "token " + user_access_token,
                                    "Accept": "application/vnd.github.machine-man-preview+json"
                                })
        return response.json()

    @staticmethod
    def get_installation_access_token(installation_id, private_key):
        integration = GithubIntegration(str(GITHUB_APP_IDENTIFIER), private_key)
        return integration.get_access_token(installation_id).token

    @staticmethod
    def verify_signature(signature, body, github_webhook_secret):
        computed_signature = "sha1=" + hmac.new(str.encode(github_webhook_secret), body, sha1).hexdigest()
        return computed_signature == signature


