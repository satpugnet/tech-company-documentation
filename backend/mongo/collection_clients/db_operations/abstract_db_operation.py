from abc import ABC


class AbstractDbOperation(ABC):
    """
    Abstract class for db operations.
    """

    def __init__(self, collection_name, collection_client):
        self._collection_name = collection_name
        self._collection_client = collection_client
