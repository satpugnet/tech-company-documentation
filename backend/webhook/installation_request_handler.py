from mongo.models.account_installation import AccountInstallation


class InstallationRequestHandler:

    def __init__(self, organisation_login):
        self.__organisation_login = organisation_login

    def enact_installation_deleted_event(self):
        AccountInstallation.remove(self.__organisation_login)
