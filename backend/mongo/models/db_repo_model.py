from mongo.mongo_client_connection import MongoClientConnection
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
            'github_account_login': self.__github_account_login,
            'repo_name': self.__repo_name,
            'sha_last_update': self.__sha_last_update
        }

    @staticmethod
    def from_json(repository):
        return DbRepoModel(
            repository['github_account_login'],
            repository['repo_name'],
            repository['sha_last_update']
        )
