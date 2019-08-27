from mongo.collection_clients.db_operation_facades.abstract_db_operation_facade import AbstractDbOperationFacade
from tools import logger


class DbUpdateOperationFacade(AbstractDbOperationFacade):
    """
    A class representing all the database update operations.
    """

    def __init__(self, collection_name, collection_client, filter_model, update_model, update_action):
        super().__init__(collection_name, collection_client)
        self.__filter_query = filter_model.to_db_json_filter_query()
        self.__update_query = update_model.to_db_json_update_query(update_action.value)

    def update_one(self):

        try:
            logger.get_logger().info("For collection %s: executing mongo operation 'update one' with filter query: %s and update query: %s", self._collection_name, self.__filter_query, self.__update_query)

            return self._collection_client.update_one(self.__filter_query, self.__update_query)

        except Exception as e:
            logger.get_logger().error(
                "Failed mongo operation 'update_one' with filter query: %s and update query: %s. Obtained the following exception: \n%s",
                self.__filter_query,
                self.__update_query,
                e
            )

    def find_one_and_update(self, return_document):

        try:
            logger.get_logger().info("For collection %s: executing mongo operation 'find one and update' with filter query: %s and update query: %s", self._collection_name, self.__filter_query, self.__update_query)

            return self._collection_client.find_one_and_update(self.__filter_query, self.__update_query, return_document=return_document)

        except Exception as e:
            logger.get_logger().error(
                "Failed mongo operation 'find_one_and_update' with filter query: %s and update query: %s. Obtained the following exception: \n%s",
                self.__filter_query,
                self.__update_query,
                e
            )

    def upsert_one(self):

        try:
            logger.get_logger().info("For collection %s: executing mongo operation 'upsert one' with filter query: %s and update query: %s", self._collection_name, self.__filter_query, self.__update_query)

            return self._collection_client.update_one(self.__filter_query, self.__update_query, upsert=True)

        except Exception as e:
            logger.get_logger().error(
                "Failed mongo operation 'upsert_one' with filter query: %s and update query: %s. Obtained the following exception: \n%s",
                self.__filter_query,
                self.__update_query,
                e
            )

