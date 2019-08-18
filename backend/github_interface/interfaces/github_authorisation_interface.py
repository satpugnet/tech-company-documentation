import requests
from github import GithubIntegration, Github

from utils.global_constant import GlobalConst


class GithubAuthorisationInterface:
    @staticmethod
    def request_user_token(client_id, client_secret, code, redirect_uri):
        print("Requesting the user token")

        params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri
        }
        response = requests.get(url="https://github.com/login/oauth/access_token", params=params)
        decoded_content = response.content.decode("utf-8")
        user_token = decoded_content[decoded_content.find("access_token=") + 13: decoded_content.find("&")]

        return user_token

    @staticmethod
    def request_user_login(user_token):
        print("Requesting the user login")

        github_account = Github(user_token)
        user = github_account.get_user()

        return user.login

    @staticmethod
    def request_installation_access_token(installation_id, private_key):
        print("Requesting the installation token")

        integration = GithubIntegration(str(GlobalConst.GITHUB_APP_IDENTIFIER), private_key)
        installation_token = integration.get_access_token(installation_id)

        return installation_token.token, installation_token.expires_at
