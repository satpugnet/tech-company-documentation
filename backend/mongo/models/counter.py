from pymongo import ReturnDocument

from mongo.mongo_client import DB


class Counter:
    """
    Represents counters for various collections

    Counters allow us to track unique ids, for example for account_installations, where we want a unique id per
    installation. See for ref https://docs.mongodb.com/v3.0/tutorial/create-an-auto-incrementing-field/

    You can add multiple counters using this collection. Simply define an ID field.
    """

    COLLECTION = DB['counter']  # Reference to the mongo collection

    MONGO_ID_FIELD = "_id"
    COUNTER_FIELD = "counter"

    # Id fields
    COUNTER_ACCOUNT_INSTALLATION_ID_FIELD = "installation_id_counter"

    @staticmethod
    def init():
        if Counter.COLLECTION.find().count() == 0:
            Counter.COLLECTION.insert({
                Counter.MONGO_ID_FIELD: Counter.COUNTER_ACCOUNT_INSTALLATION_ID_FIELD,
                Counter.COUNTER_FIELD: 0
            })

    @staticmethod
    def get_next_account_installation_id():
        find = {
            Counter.MONGO_ID_FIELD: Counter.COUNTER_ACCOUNT_INSTALLATION_ID_FIELD
        }

        update = {
            "$inc": {
                Counter.COUNTER_FIELD: 1
            }
        }

        return Counter.COLLECTION.find_one_and_update(find, update, return_document=ReturnDocument.AFTER)[Counter.COUNTER_FIELD]


# Always init the model before using it
Counter.init()
