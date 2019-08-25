from abc import ABC


class AbstractDbOperation(ABC):
    """
    Abstract class for db operations.
    """

    def __init__(self, collection_client):
        self._collection_client = collection_client
