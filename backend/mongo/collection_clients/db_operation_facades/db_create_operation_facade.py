from mongo.collection_clients.db_operation_facades.abstract_db_operation_facade import AbstractDbOperationFacade
from tools import logger


class DbCreateOperationFacade(AbstractDbOperationFacade):
    """
    A class representing all the database create operations.
    """

    def __init__(self, collection_name, collection_client, insert_model):
        super().__init__(collection_name, collection_client)
        self.__insert_query = insert_model.to_db_json_insert_query()

    def insert_one(self):

        try:
            logger.get_logger().info("For collection %s: executing mongo operation 'insert one' with insert query: %s", self._collection_name, self.__insert_query)
            return self._collection_client.insert_one(self.__insert_query)

        except Exception as e:
            logger.get_logger().error("Failed mongo operation 'insert_one' with insert query: %s. Obtained the following exception: %s", self.__insert_query, e)
