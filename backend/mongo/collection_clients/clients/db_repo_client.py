from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.constants.db_update_actions import DbUpdateActions
from mongo.models.db_repo_model import DbRepoModel


# TODO: We need to include is_private and the list of collaborators in this so that we can filter access for user
#  accessing the doc of other users
class DbRepoClient(AbstractDbCollectionClient):
    """
    A client for the database repo collection.
    """

    def __init__(self):
        super().__init__('repo', DbRepoModel)

    def find(self, github_account_login):
        return self._find(
            DbRepoModel(
                github_account_login=github_account_login
            )
        )

    def find_one(self, name):
        return self._find_one(
            DbRepoModel(
                name=name
            )
        )

    def insert_one(self, github_account_login, name):
        return self._insert_one(
            DbRepoModel(
                github_account_login=github_account_login,
                name=name,
                sha_last_update=""
            )
        )

    def upsert_one_sha_last_update(self, github_account_login, name, sha_last_update):
        return self._upsert_one(
            DbRepoModel(
                github_account_login=github_account_login,
                name=name
            ),
            DbRepoModel(
                sha_last_update=sha_last_update
            ),
            DbUpdateActions.SET_ACTION
        )

    def remove(self, github_account_login):
        return self._remove(
            DbRepoModel(
                github_account_login=github_account_login
            )
        )
