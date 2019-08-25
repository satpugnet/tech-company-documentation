from abc import ABC

from mongo.collection_clients.db_operation_facades.db_create_operation_facade import DbCreateOperationFacade
from mongo.collection_clients.db_operation_facades.db_delete_operation_facade import DbDeleteOperationFacade
from mongo.collection_clients.db_operation_facades.db_read_operation_facade import DbReadOperationFacade
from mongo.collection_clients.db_operation_facades.db_update_operation_facade import DbUpdateOperationFacade
from mongo.mongo_client_connection import DB


class AbstractDbCollectionClient(ABC):
    """
    Abstract class for a collection client.
    """

    def __init__(self, collection_name, model_class):
        self.__collection_name = collection_name
        self.__client = DB[collection_name]
        self.__model_class = model_class

    def _find_all(self):
        return [self.__model_class.from_json(document) for document in DbReadOperationFacade(self.__collection_name, self.__client, self.__model_class()).find()]

    def _find(self, filter_model):
        return [self.__model_class.from_json(document) for document in DbReadOperationFacade(self.__collection_name, self.__client, filter_model).find()]

    def _find_one(self, filter_model):
        document = DbReadOperationFacade(self.__collection_name, self.__client, filter_model).find_one()
        return self.__model_class.from_json(document) if document else None

    def _insert_one(self, insert_model):
        return DbCreateOperationFacade(self.__collection_name, self.__client, insert_model).insert_one()

    def _find_one_and_update(self, filter_model, update_model, update_action, return_document):
        return DbUpdateOperationFacade(self.__collection_name, self.__client, filter_model, update_model, update_action).find_one_and_update(return_document)

    def _upsert_one(self, filter_model, update_model, update_action):
        return DbUpdateOperationFacade(self.__collection_name, self.__client, filter_model, update_model, update_action).upsert_one()

    def _update_one(self, filter_model, update_model, update_action):
        return DbUpdateOperationFacade(self.__collection_name, self.__client, filter_model, update_model, update_action).update_one()

    def _remove(self, filter_model):
        return DbDeleteOperationFacade(self.__collection_name, self.__client, filter_model).remove()
