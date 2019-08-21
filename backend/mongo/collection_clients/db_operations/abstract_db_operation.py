from abc import ABC


class AbstractDbOperation(ABC):

    def __init__(self, collection_client):
        self._collection_client = collection_client
