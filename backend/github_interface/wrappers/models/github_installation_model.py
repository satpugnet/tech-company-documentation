from mongo.constants.model_fields import ModelFields

from tools.json.jsonable import Jsonable


class GithubInstallationModel(Jsonable):
    """
    Represent a github installation.
    """

    ID_FIELD = ModelFields.ID
    GITHUB_ACCOUNT_LOGIN_FIELD = ModelFields.GITHUB_ACCOUNT_LOGIN

    def __init__(self, id, github_account_login):
        self.__id = id
        self.__github_account_login = github_account_login

    @property
    def id(self):
        return self.__id

    @property
    def github_account_login(self):
        return self.__github_account_login

    def to_json(self):
        return {
            GithubInstallationModel.ID_FIELD: self.id,
            GithubInstallationModel.GITHUB_ACCOUNT_LOGIN_FIELD: self.github_account_login
        }
