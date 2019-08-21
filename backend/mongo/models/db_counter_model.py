from mongo.constants.db_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


class DbCounterModel(AbstractDbCollectionModel):
    """
    Represents counters for various collections

    Counters allow us to track unique ids, for example for account_installations, where we want a unique id per
    installation. See for ref https://docs.mongodb.com/v3.0/tutorial/create-an-auto-incrementing-field/

    You can add multiple counters using this collection. Simply define an ID field.
    """

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
            ModelFields.MONGO_ID: self.__id,
            ModelFields.COUNTER: self.__counter
        }

    @staticmethod
    def from_json(counter):
        return DbCounterModel(
            counter[ModelFields.MONGO_ID],
            counter[ModelFields.COUNTER]
        )
