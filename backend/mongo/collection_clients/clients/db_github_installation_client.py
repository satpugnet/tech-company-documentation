from datetime import datetime, timezone

from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.collection_clients.clients.db_counter_client import DbCounterClient
from mongo.constants.db_update_actions import DbUpdateActions
from mongo.models.db_github_installation_model import DbGithubInstallationModel


# TODO: remove the logic for the expire token from this class
class DbGithubInstallationClient(AbstractDbCollectionClient):
    """
    A client for the database github installation collection.
    """

    def __init__(self):
        super().__init__('github_installation', DbGithubInstallationModel)

    def find_one(self, github_account_login):

        return self._find_one(
            DbGithubInstallationModel(
                github_account_login=github_account_login
            )
        )

    def insert_one(self, github_account_login, id, token, expires_at):
        mongo_id = DbCounterClient().get_next_account_installation_id()

        return self._insert_one(
            DbGithubInstallationModel(
                mongo_id=mongo_id,
                github_account_login=github_account_login,
                id=id,
                token=token,
                expires_at=expires_at
            )
        )

    def remove(self, github_account_login):
        return self._remove(
            DbGithubInstallationModel(
                github_account_login=github_account_login
            )
        )

    def update_one_token(self, mongo_id, token, expires_at):
        return self._update_one(
            DbGithubInstallationModel(
                mongo_id=mongo_id
            ),
            DbGithubInstallationModel(
                token=token,
                expires_at=expires_at
            ),
            DbUpdateActions.SET_ACTION
        )

    def __is_expired(self, expires_at):
        return expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc)


