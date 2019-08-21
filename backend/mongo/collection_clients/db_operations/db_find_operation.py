from mongo.collection_clients.db_operations.abstract_db_operation import AbstractDbOperation
from tools import logger


class DbFindOperation(AbstractDbOperation):

    def __init__(self, collection_client, filter_model):
        super().__init__(collection_client)
        self.__filter_query = filter_model.to_db_json_filter_query()

    def find(self):
        try:
            return self._collection_client.find({})
        except Exception:
            logger.get_logger().error("Failed to find with query %s", self.__filter_query)

    def find_one(self):
        try:
            return self._collection_client.find_one(self.__filter_query)
        except Exception:
            logger.get_logger().error("Failed to find one with query %s", self.__filter_query)
