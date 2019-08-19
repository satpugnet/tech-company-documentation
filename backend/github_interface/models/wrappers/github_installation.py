from utils.json.sensitive_jsonable import SensitiveJsonable


class GithubInstallation(SensitiveJsonable):
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
            "id": self.id,
            "github_account_login": self.github_account_login
        }
