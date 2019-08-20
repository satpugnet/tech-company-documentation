from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.constants.db_new_values_actions import DbNewValuesActions
from mongo.models.db_repo_model import DbRepoModel


class DbRepoClient(AbstractDbCollectionClient):
    def __init__(self):
        super().__init__('repo', DbRepoModel)

    def upsert(self, github_account_login, name):
        return self._upsert(
            DbRepoModel(
                github_account_login=github_account_login,
                name=name
            ),
            DbRepoModel(
                github_account_login=github_account_login,
                name=name,
                sha_last_update=""
            ),
            DbNewValuesActions.SET_ACTION
        )

    def upsert_sha_last_update_only(self, github_account_login, name, sha_last_update):
        return self._upsert(
            DbRepoModel(
                github_account_login=github_account_login,
                name=name
            ),
            DbRepoModel(
                sha_last_update=sha_last_update
            ),
            DbNewValuesActions.SET_ACTION
        )

    def find_one(self, name):
        return self._find_one(
            DbRepoModel(
                name=name
            )
        )

    def remove(self, github_account_login):
        return self._remove(
            DbRepoModel(
                github_account_login=github_account_login
            )
        )