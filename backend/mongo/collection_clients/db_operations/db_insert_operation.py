from mongo.collection_clients.db_operations.abstract_db_operation import AbstractDbOperation
from tools import logger


class DbInsertOperation(AbstractDbOperation):
    def __init__(self, collection_client, update_model):
        super().__init__(collection_client)
        self.__insert_query = update_model.to_db_json_insert_query()

    def insert_one(self):
        try:
            return self._collection_client.insert_one(self.__insert_query)
        except Exception:
            logger.get_logger().error("Failed to insert one with values %s", self.__insert_query)
