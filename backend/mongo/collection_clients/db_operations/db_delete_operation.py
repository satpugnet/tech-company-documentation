from mongo.collection_clients.db_operations.abstract_db_operation import AbstractDbOperation
from tools import logger


class DbDeleteOperation(AbstractDbOperation):

    def __init__(self, collection_client, filter_model):
        super().__init__(collection_client)
        self.__filter_query = filter_model.to_db_json_filter_query()

    def remove(self):
        try:
            return self._collection_client.remove(self.__filter_query)
        except Exception:
            logger.get_logger().error("Failed to remove with query %s", self.__filter_query)
