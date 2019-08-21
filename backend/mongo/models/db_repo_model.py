from mongo.constants.db_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


class DbRepoModel(AbstractDbCollectionModel):
    """
    Represents a github repository
    """

    def __init__(self, github_account_login=None, name=None, sha_last_update=None):
        self.__github_account_login = github_account_login
        self.__name = name
        self.__sha_last_update = sha_last_update

    @property
    def github_account_login(self):
        return self.__github_account_login

    @property
    def name(self):
        return self.__name

    @property
    def sha_last_update(self):
        return self.__sha_last_update

    def to_json(self):
        return {
            ModelFields.GITHUB_ACCOUNT_LOGIN: self.__github_account_login,
            ModelFields.NAME: self.__name,
            ModelFields.SHA_LAST_UPDATE: self.__sha_last_update
        }

    @staticmethod
    def from_json(repository):
        return DbRepoModel(
            repository[ModelFields.GITHUB_ACCOUNT_LOGIN],
            repository[ModelFields.NAME],
            repository[ModelFields.SHA_LAST_UPDATE]
        )
