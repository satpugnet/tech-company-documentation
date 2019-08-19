from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.constants.db_new_values_actions import DbNewValuesActions
from mongo.models.db_user_model import DbUserModel


class DbUserClient(AbstractDbCollectionClient):
    """
    Represents a user
    """

    def __init__(self):
        super().__init__('user', DbUserModel)

    def upsert_user_token(self, login, user_token):
        return self._upsert(
            DbUserModel(
                login=login
            ),
            DbUserModel(
                user_token=user_token
            ),
            DbNewValuesActions.SET_ACTION
        )

    def find_one(self, login):
        return self._find_one(
            DbUserModel(
                login=login
            )
        )

