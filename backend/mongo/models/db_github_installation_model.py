from utils.json.jsonable import Jsonable


# TODO create a parent class for all models to avoid DRY
class DbGithubInstallationModel(Jsonable):
    """
    Represents an account installation
    """

    MONGO_ID_FIELD = "_id"
    GITHUB_ACCOUNT_LOGIN_FIELD = "github_account_login"
    INSTALLATION_ID_FIELD = "installation_id"
    INSTALLATION_TOKEN_FIELD = "installation_token"
    EXPIRES_AT_FIELD = "expires_at"

    def __init__(self, mongo_id=None, github_account_login=None, installation_id=None, installation_token=None, expires_at=None):
        self.__mongo_id = mongo_id
        self.__github_account_login = github_account_login
        self.__installation_id = installation_id
        self.__installation_token = installation_token  # Anytime this is accessed, the expires_at must be checked
        self.__expires_at = expires_at

    @property
    def mongo_id(self):
        return self.__mongo_id

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
            DbGithubInstallationModel.MONGO_ID_FIELD: self.mongo_id,
            DbGithubInstallationModel.GITHUB_ACCOUNT_LOGIN_FIELD: self.github_account_login,
            DbGithubInstallationModel.INSTALLATION_ID_FIELD: self.installation_id,
            DbGithubInstallationModel.INSTALLATION_TOKEN_FIELD: self.installation_token,
            DbGithubInstallationModel.EXPIRES_AT_FIELD: self.expires_at
        }

    @staticmethod
    def from_json(installation):
        return DbGithubInstallationModel(
            installation[DbGithubInstallationModel.MONGO_ID_FIELD],
            installation[DbGithubInstallationModel.GITHUB_ACCOUNT_LOGIN_FIELD],
            installation[DbGithubInstallationModel.INSTALLATION_ID_FIELD],
            installation[DbGithubInstallationModel.INSTALLATION_TOKEN_FIELD],
            installation[DbGithubInstallationModel.EXPIRES_AT_FIELD]
        )
