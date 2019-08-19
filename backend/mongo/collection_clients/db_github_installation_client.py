from datetime import datetime, timezone

from github_interface.interfaces.github_authorisation_interface import GithubAuthorisationInterface
from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.collection_clients.db_counter_client import DbCounterClient
from mongo.constants.db_new_values_actions import DbNewValuesActions
from mongo.models.db_github_installation_model import DbGithubInstallationModel
from utils.file_system_interface import FileSystemInterface


# TODO: remove the logic for the expire token from this class
class DbGithubInstallationClient(AbstractDbCollectionClient):
    """
    Represents a github installation
    """

    def __init__(self):
        super().__init__('github_installation', DbGithubInstallationModel)

    def remove(self, github_account_login):
        return self._remove(
            DbGithubInstallationModel(
                github_account_login=github_account_login
            )
        )

    def find_one(self, github_account_login):
        installation = self._find_one(
            DbGithubInstallationModel(
                github_account_login=github_account_login
            )
        )

        if self.__is_expired(installation.expires_at):
            self.__update_installation_token(installation.mongo_id, installation.installation_id)
            return self.__find_one(github_account_login)
        else:
            return installation

    def insert_if_not_exist(self, github_account_login, installation_id):
        if self.__find_one(github_account_login) is not None:
            return

        self.__upsert_updated_installation(github_account_login, installation_id)

    def __upsert_updated_installation(self, github_account_login, installation_id):
        installation_token, expires_at = GithubAuthorisationInterface.request_installation_access_token(
            installation_id,
            FileSystemInterface.load_private_key()
        )

        mongo_id = DbCounterClient().get_next_account_installation_id()

        return self._upsert(
            DbGithubInstallationModel(
                github_account_login=github_account_login
            ),
            DbGithubInstallationModel(
                mongo_id=mongo_id,
                github_account_login=github_account_login,
                installation_id=installation_id,
                installation_token=installation_token,
                expires_at=expires_at
            ),
            DbNewValuesActions.SET_ACTION
        )

    def __update_installation_token(self, mongo_id, installation_id):
        installation_token, expires_at = GithubAuthorisationInterface.request_installation_access_token(
            installation_id,
            FileSystemInterface.load_private_key()
        )

        return self._update_one(
            DbGithubInstallationModel(
                mongo_id=mongo_id
            ),
            DbGithubInstallationModel(
                installation_token=installation_token,
                expires_at=expires_at
            ),
            DbNewValuesActions.SET_ACTION
        )

    def __find_one(self, github_account_login):
        return self._find_one(
            DbGithubInstallationModel(
                github_account_login=github_account_login)
        )

    def __is_expired(self, expires_at):
        return expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc)


