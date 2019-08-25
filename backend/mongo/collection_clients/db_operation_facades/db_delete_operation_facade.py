from mongo.collection_clients.db_operation_facades.abstract_db_operation_facade import AbstractDbOperationFacade
from tools import logger


class DbDeleteOperationFacade(AbstractDbOperationFacade):
    """
    A class representing all the database delete operations.
    """

    def __init__(self, collection_name, collection_client, filter_model):
        super().__init__(collection_name, collection_client)
        self.__filter_query = filter_model.to_db_json_filter_query()

    def remove(self):

        try:
            logger.get_logger().info("For collection %s: executing mongo operation 'remove' with filter query: %s", self._collection_name, self.__filter_query)
            return self._collection_client.remove(self.__filter_query)

        except Exception as e:
            logger.get_logger().error("Failed mongo operation 'remove' with filter query: %s. Obtained the following exception:\n%s", self.__filter_query, e)
