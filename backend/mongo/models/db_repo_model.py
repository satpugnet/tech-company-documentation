from mongo.constants.db_fields import DbFields
from utils.json.jsonable import Jsonable


class DbRepoModel(Jsonable):
    """
    Represents a github repository, used to keep track of the state of the internal db for this repository
    """

    def __init__(self, github_account_login=None, repo_name=None, sha_last_update=None):
        self.__github_account_login = github_account_login
        self.__repo_name = repo_name
        self.__sha_last_update = sha_last_update

    @property
    def github_account_login(self):
        return self.__github_account_login

    @property
    def repo_name(self):
        return self.__repo_name

    @property
    def sha_last_update(self):
        return self.__sha_last_update

    def to_json(self):
        return {
            DbFields.GITHUB_ACCOUNT_LOGIN_FIELD: self.__github_account_login,
            DbFields.REPO_NAME_FIELD: self.__repo_name,
            DbFields.SHA_LAST_UPDATE_FIELD: self.__sha_last_update
        }

    @staticmethod
    def from_json(repository):
        return DbRepoModel(
            repository[DbFields.GITHUB_ACCOUNT_LOGIN_FIELD],
            repository[DbFields.REPO_NAME_FIELD],
            repository[DbFields.SHA_LAST_UPDATE_FIELD]
        )
