from mongo.constants.db_fields import ModelFields
from utils.json.jsonable import Jsonable


# TODO create a parent class for all wrappers to avoid DRY
class DbGithubInstallationModel(Jsonable):
    """
    Represents a github account installation with its associated token
    """

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
            ModelFields.MONGO_ID: self.mongo_id,
            ModelFields.GITHUB_ACCOUNT_LOGIN: self.github_account_login,
            ModelFields.ID: self.id,
            ModelFields.TOKEN: self.token,
            ModelFields.EXPIRES_AT: self.expires_at
        }

    @staticmethod
    def from_json(installation):
        return DbGithubInstallationModel(
            installation[ModelFields.MONGO_ID],
            installation[ModelFields.GITHUB_ACCOUNT_LOGIN],
            installation[ModelFields.ID],
            installation[ModelFields.TOKEN],
            installation[ModelFields.EXPIRES_AT]
        )
