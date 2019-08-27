from mongo.constants.model_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


class DbRepoModel(AbstractDbCollectionModel):
    """
    Represents a github repository.
    """

    GITHUB_ACCOUNT_LOGIN_FIELD = ModelFields.GITHUB_ACCOUNT_LOGIN
    NAME_FIELD = ModelFields.NAME
    SHA_LAST_UPDATE_FIELD = ModelFields.SHA_LAST_UPDATE

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
            DbRepoModel.GITHUB_ACCOUNT_LOGIN_FIELD: self.__github_account_login,
            DbRepoModel.NAME_FIELD: self.__name,
            DbRepoModel.SHA_LAST_UPDATE_FIELD: self.__sha_last_update
        }

    @staticmethod
    def from_json(repository):
        return DbRepoModel(
            repository[DbRepoModel.GITHUB_ACCOUNT_LOGIN_FIELD],
            repository[DbRepoModel.NAME_FIELD],
            repository[DbRepoModel.SHA_LAST_UPDATE_FIELD]
        )
