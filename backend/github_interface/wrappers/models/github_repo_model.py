from mongo.constants.model_fields import ModelFields

from tools.json.jsonable import Jsonable


class GithubRepoModel(Jsonable):
    """
    Represent a github repository
    """

    GITHUB_ACCOUNT_LOGIN_FIELD = ModelFields.GITHUB_ACCOUNT_LOGIN
    NAME_FIELD = ModelFields.NAME
    FULL_NAME_FIELD = ModelFields.FULL_NAME
    OWNER_TYPE_FIELD = ModelFields.OWNER_TYPE
    PRIVATE_FIELD = ModelFields.PRIVATE

    def __init__(self, github_account_login, name, full_name, owner_type, private):
        self.__github_account_login = github_account_login
        self.__name = name
        self.__full_name = full_name
        self.__owner_type = owner_type
        self.__private = private

    @property
    def github_account_login(self):
        return self.__github_account_login

    @property
    def name(self):
        return self.__name

    @property
    def full_name(self):
        return self.__full_name

    @property
    def owner_type(self):
        return self.__owner_type

    @property
    def private(self):
        return self.__private

    def to_json(self):
        return {
            GithubRepoModel.GITHUB_ACCOUNT_LOGIN_FIELD: self.github_account_login,
            GithubRepoModel.NAME_FIELD: self.name,
            GithubRepoModel.FULL_NAME_FIELD: self.full_name,
            GithubRepoModel.OWNER_TYPE_FIELD: self.owner_type,
            GithubRepoModel.PRIVATE_FIELD: self.private
        }
