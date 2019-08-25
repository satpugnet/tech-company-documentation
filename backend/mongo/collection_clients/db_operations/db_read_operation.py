from mongo.collection_clients.db_operations.abstract_db_operation import AbstractDbOperation
from tools import logger


class DbReadOperation(AbstractDbOperation):
    """
    A class representing all the database read operations.
    """

    def __init__(self, collection_name, collection_client, filter_model):
        super().__init__(collection_name, collection_client)
        self.__filter_query = filter_model.to_db_json_filter_query()

    def find(self):

        try:
            logger.get_logger().info("For collection %s: executing mongo operation 'find' with filter query: %s", self._collection_name, self.__filter_query)
            return self._collection_client.find(self.__filter_query)

        except Exception as e:
            logger.get_logger().error("Failed mongo operation 'find' with filter query: %s. Obtained the following exception: %s", self.__filter_query, e)

    def find_one(self):

        try:
            logger.get_logger().info("For collection %s: executing mongo operation 'find one' with filter query: %s", self._collection_name, self.__filter_query)
            return self._collection_client.find_one(self.__filter_query)

        except Exception as e:
            logger.get_logger().error("Failed mongo operation 'find_one' with filter query %s. Obtained the following exception: %s", self.__filter_query, e)
