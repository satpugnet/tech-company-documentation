from mongo.constants.db_fields import DbFields
from utils.json.sensitive_jsonable import SensitiveJsonable


class GithubInstallationModel(SensitiveJsonable):

    def __init__(self, id, github_account_login):
        self.__id = id
        self.__github_account_login = github_account_login

    @property
    def id(self):
        return self.__id

    @property
    def github_account_login(self):
        return self.__github_account_login

    def non_sensitive_data_to_json(self):
        return {
            DbFields.ID_FIELD: self.id,
            DbFields.GITHUB_ACCOUNT_LOGIN_FIELD: self.github_account_login
        }
