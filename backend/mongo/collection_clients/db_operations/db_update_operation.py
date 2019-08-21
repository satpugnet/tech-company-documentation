from mongo.collection_clients.db_operations.abstract_db_operation import AbstractDbOperation
from tools import logger


class DbUpdateOperation(AbstractDbOperation):

    def __init__(self, collection_client, filter_model, update_model, update_action):
        super().__init__(collection_client)
        self.__filter_query = filter_model.to_db_json_filter_query()
        self.__update_query = update_model.to_db_json_update_query(update_action)

    def update_one(self):
        try:
            return self._collection_client.update_one(self.__filter_query, self.__update_query)
        except Exception:
            logger.get_logger().error("Failed to update one with query %s and values %s", self.__filter_query, self.__update_query)

    def find_one_and_update(self, return_document):
        try:
            return self._collection_client.find_one_and_update(self.__filter_query, self.__update_query, return_document=return_document)
        except Exception:
            logger.get_logger().error("Failed to find one and update with query %s and values %s", self.__filter_query, self.__update_query)

    def upsert_one(self):
        try:
            return self._collection_client.update_one(self.__filter_query, self.__update_query, upsert=True)
        except Exception:
            logger.get_logger().error("Failed to upsert one with query %s and values %s", self.__filter_query, self.__update_query)

