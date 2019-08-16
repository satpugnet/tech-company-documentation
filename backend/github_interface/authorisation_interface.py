import requests
import hmac
from hashlib import sha1
from github import GithubIntegration

from utils.constants import GITHUB_APP_IDENTIFIER


class GithubAuthorisationInterface:
    @staticmethod
    def get_user_token(client_id, client_secret, code, redirect_uri):
        params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri
        }
        r = requests.get(url="https://github.com/login/oauth/access_token", params=params)
        content = r.content.decode("utf-8")
        user_token = content[content.find("access_token=") + 13: content.find("&")]

        return user_token

    @staticmethod
    def get_installation_access_token(installation_id, private_key):
        integration = GithubIntegration(str(GITHUB_APP_IDENTIFIER), private_key)
        installation_token = integration.get_access_token(installation_id)
        return installation_token.token, installation_token.expires_at

    @staticmethod
    def verify_signature(signature, body, github_webhook_secret):
        computed_signature = "sha1=" + hmac.new(str.encode(github_webhook_secret), body, sha1).hexdigest()
        return computed_signature == signature
