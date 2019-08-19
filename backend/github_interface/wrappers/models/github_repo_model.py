from mongo.constants.db_fields import DbFields
from utils.json.sensitive_jsonable import SensitiveJsonable


class GithubRepoModel(SensitiveJsonable):

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

    def non_sensitive_data_to_json(self):
        return {
            DbFields.GITHUB_ACCOUNT_LOGIN_FIELD: self.github_account_login,
            DbFields.NAME_FIELD: self.name,
            DbFields.FULL_NAME_FIELD: self.full_name,
            DbFields.OWNER_TYPE_FIELD: self.owner_type,
            DbFields.PRIVATE_FIELD: self.private
        }
