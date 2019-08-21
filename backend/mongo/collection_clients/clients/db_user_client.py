from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.constants.db_update_actions import DbUpdateActions
from mongo.models.db_user_model import DbUserModel


class DbUserClient(AbstractDbCollectionClient):
    """
    Represents a user
    """

    def __init__(self):
        super().__init__('user', DbUserModel)

    def find_one(self, login):
        return self._find_one(
            DbUserModel(
                login=login
            )
        )

    def upsert_one_user_token(self, login, token):
        return self._upsert_one(
            DbUserModel(
                login=login
            ),
            DbUserModel(
                token=token
            ),
            DbUpdateActions.SET_ACTION
        )

