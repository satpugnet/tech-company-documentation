from abc import ABC


class AbstractDbOperationFacade(ABC):
    """
    A facade for communicating with the mongo database.
    ALL CALLS TO THE MONGO DATABASE API SHOULD BE MADE USING THIS CLASS AND SUBCLASSES.
    """

    def __init__(self, collection_name, collection_client):
        self._collection_name = collection_name
        self._collection_client = collection_client
