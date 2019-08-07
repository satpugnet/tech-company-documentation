from utils.json.jsonable import Jsonable


class GithubInstallation(Jsonable):
    def __init__(self, installation):
        self._id = installation["id"]
        self._account = self.__initialise_account(installation["account"])

    @property
    def id(self):
        return self._id

    @property
    def account(self):
        return self._account

    def __initialise_account(self, installation_account):
        return {
            "login": installation_account["login"]
        }

    def to_json(self):
        new_json = {
            "id": self.id,
            "account": self.account
        }
        return new_json
