from mongo.constants.db_fields import DbFields
from utils.json.jsonable import Jsonable


class DbCounterModel(Jsonable):
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
            DbFields.MONGO_ID_FIELD: self.__id,
            DbFields.COUNTER_FIELD: self.__counter
        }

    @staticmethod
    def from_json(counter):
        return DbCounterModel(
            counter[DbFields.MONGO_ID_FIELD],
            counter[DbFields.COUNTER_FIELD]
        )
