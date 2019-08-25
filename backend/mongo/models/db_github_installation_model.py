from mongo.constants.model_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


class DbGithubInstallationModel(AbstractDbCollectionModel):
    """
    Represents a github account installation with its associated token.
    """

    MONGO_ID_FIELD = ModelFields.MONGO_ID
    GITHUB_ACCOUNT_LOGIN_FIELD = ModelFields.GITHUB_ACCOUNT_LOGIN
    ID_FIELD = ModelFields.ID
    TOKEN_FIELD = ModelFields.TOKEN
    EXPIRES_AT_FIELD = ModelFields.EXPIRES_AT

    def __init__(self, mongo_id=None, github_account_login=None, id=None, token=None, expires_at=None):
        self.__mongo_id = mongo_id
        self.__github_account_login = github_account_login
        self.__id = id
        self.__token = token  # Anytime this is accessed, the expires_at must be checked
        self.__expires_at = expires_at

    @property
    def mongo_id(self):
        return self.__mongo_id

    @property
    def github_account_login(self):
        return self.__github_account_login

    @property
    def id(self):
        return self.__id

    @property
    def token(self):
        return self.__token

    @property
    def expires_at(self):
        return self.__expires_at

    def to_json(self):
        return {
            DbGithubInstallationModel.MONGO_ID_FIELD: self.mongo_id,
            DbGithubInstallationModel.GITHUB_ACCOUNT_LOGIN_FIELD: self.github_account_login,
            DbGithubInstallationModel.ID_FIELD: self.id,
            DbGithubInstallationModel.TOKEN_FIELD: self.token,
            DbGithubInstallationModel.EXPIRES_AT_FIELD: self.expires_at
        }

    @staticmethod
    def from_json(installation):
        return DbGithubInstallationModel(
            installation[DbGithubInstallationModel.MONGO_ID_FIELD],
            installation[DbGithubInstallationModel.GITHUB_ACCOUNT_LOGIN_FIELD],
            installation[DbGithubInstallationModel.ID_FIELD],
            installation[DbGithubInstallationModel.TOKEN_FIELD],
            installation[DbGithubInstallationModel.EXPIRES_AT_FIELD]
        )
