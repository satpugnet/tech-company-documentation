from pymongo import ReturnDocument

from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.constants.db_fields import DbFields
from mongo.constants.db_new_values_actions import DbNewValuesActions
from mongo.models.db_counter_model import DbCounterModel


class DbCounterClient(AbstractDbCollectionClient):

    # Id value
    COUNTER_ACCOUNT_INSTALLATION_ID_FIELD = "installation_id_counter"

    def __init__(self):
        super().__init__('counter', DbCounterModel)

    def init(self):
        if len(self.find_all()) == 0:
            self.insert_one(DbCounterModel(
                id=DbCounterClient.COUNTER_ACCOUNT_INSTALLATION_ID_FIELD,
                counter=0
            ))

    def get_next_account_installation_id(self):
        db_counter = self._find_one_and_update(
            DbCounterModel(
                id=DbCounterClient.COUNTER_ACCOUNT_INSTALLATION_ID_FIELD
            ),
            DbCounterModel(
                counter=1
            ),
            ReturnDocument.AFTER,
            DbNewValuesActions.INC_ACTION
        )
        return db_counter[DbFields.COUNTER_FIELD]


# Always init the model before using it
DbCounterClient().init()
