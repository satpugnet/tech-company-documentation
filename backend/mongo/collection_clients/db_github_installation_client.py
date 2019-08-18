from github_interface.interfaces.github_authorisation_interface import GithubAuthorisationInterface
from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.models.db_github_installation_model import DbGithubInstallationModel
from utils.file_system_interface import FileSystemInterface
from datetime import datetime, timezone


# TODO: remove the logic for the expire token from this class
class DbGithubInstallationClient(AbstractDbCollectionClient):
    """
    Represents a github installation
    """

    def __init__(self):
        super().__init__('github_installation', DbGithubInstallationModel)

    def remove(self, github_account_login):
        return self._remove(DbGithubInstallationModel(github_account_login=github_account_login))

    def find_one(self, github_account_login):
        installation = self._find_one(DbGithubInstallationModel(github_account_login=github_account_login))

        if self.__is_expired(installation.expires_at):
            self.__upsert_updated_installation(github_account_login, installation.installation_id)
            return self.__find_one(github_account_login)
        else:
            return installation

    def insert_if_not_exist(self, github_account_login, installation_id):
        if self.__find_one(github_account_login) is not None:
            return

        self.__upsert_updated_installation(github_account_login, installation_id)

    def __upsert_updated_installation(self, github_account_login, installation_id):
        private_key = FileSystemInterface.load_private_key()
        installation_token, expires_at = GithubAuthorisationInterface.request_installation_access_token(installation_id,
                                                                                                        private_key)

        return self._upsert(DbGithubInstallationModel(github_account_login=github_account_login),
                            DbGithubInstallationModel(github_account_login=github_account_login, installation_id=installation_id,
                                                      installation_token=installation_token, expires_at=expires_at))

    def __find_one(self, github_account_login):
        return self._find_one(DbGithubInstallationModel(github_account_login=github_account_login))

    def __is_expired(self, expires_at):
        return expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc)


