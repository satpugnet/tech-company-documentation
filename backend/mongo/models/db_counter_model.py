from mongo.constants.model_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


class DbCounterModel(AbstractDbCollectionModel):
    """
    Represents counters for various collections

    Counters allow us to track unique ids, for example for account_installations, where we want a unique id per
    installation. See for ref https://docs.mongodb.com/v3.0/tutorial/create-an-auto-incrementing-field/

    You can add multiple counters using this collection. Simply define an ID field.
    """

    MONGO_ID_FIELD = ModelFields.MONGO_ID
    COUNTER_FIELD = ModelFields.COUNTER

    def __init__(self, id=None, counter=None):
        self.__id = id
        self.__counter = counter

    @property
    def id(self):
        return self.__id

    @property
    def counter(self):
        return self.__counter

    def to_json(self):
        return {
            DbCounterModel.MONGO_ID_FIELD: self.__id,
            DbCounterModel.COUNTER_FIELD: self.__counter
        }

    @staticmethod
    def from_json(counter):
        return DbCounterModel(
            counter[DbCounterModel.MONGO_ID_FIELD],
            counter[DbCounterModel.COUNTER_FIELD]
        )
