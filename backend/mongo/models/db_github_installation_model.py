from utils.json.jsonable import Jsonable


# TODO create a parent class for all models to avoid DRY
class DbGithubInstallationModel(Jsonable):
    """
    Represents an account installation
    """

    def __init__(self, github_account_login=None, installation_id=None, installation_token=None, expires_at=None):
        self.__github_account_login = github_account_login
        self.__installation_id = installation_id
        self.__installation_token = installation_token  # Anytime this is accessed, the expires_at must be checked
        self.__expires_at = expires_at

    @property
    def github_account_login(self):
        return self.__github_account_login

    @property
    def installation_id(self):
        return self.__installation_id

    @property
    def installation_token(self):
        return self.__installation_token

    @property
    def expires_at(self):
        return self.__expires_at

    def to_json(self):
        return {
            'github_account_login': self.github_account_login,
            'installation_id': self.installation_id,
            'installation_token': self.installation_token,
            'expires_at': self.expires_at
        }

    @staticmethod
    def from_json(installation):
        return DbGithubInstallationModel(
            installation['github_account_login'],
            installation['installation_id'],
            installation['installation_token'],
            installation['expires_at']
        )
