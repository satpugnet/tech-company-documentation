from mongo.mongo_client_connection import MongoClientConnection


class AbstractDbCollectionClient:

    def __init__(self, collection_name, model_class):
        self.__collection_client = MongoClientConnection.DB[collection_name]
        self.__model_class = model_class

    def find_all(self):
        documents = self.__find({})

        return [self.__model_class.from_json(document) for document in documents]

    def insert_one(self, new_values_model):
        new_values_model = self.__remove_none_fields(new_values_model.to_json())
        return self.__insert_one(new_values_model)

    def _find(self, query_model):
        query_model_json = self.__convert_to_query(query_model.to_json())
        documents = self.__find(query_model_json)

        return [self.__model_class.from_json(document) for document in documents]

    def _find_one(self, query_model):
        query_model_json = self.__convert_to_query(query_model.to_json())
        document = self.__find_one(query_model_json)

        return self.__model_class.from_json(document) if document else None

    #TODO: convert this to upsert_one
    def _upsert(self, query_model, new_values_model):
        query_model_json = self.__convert_to_query(query_model.to_json())
        new_values_model_json = self.__convert_to_query_value(new_values_model.to_json())

        return self.__upsert(query_model_json, {"$set": new_values_model_json})

    def _update_one(self, query_model, new_values_model):
        query_model_json = self.__convert_to_query(query_model.to_json())
        new_values_model_json = self.__convert_to_query_value(new_values_model.to_json())

        return self.__update_one(query_model_json, {"$set": new_values_model_json})

    def _remove(self, query_model):
        query_model_json = self.__convert_to_query(query_model.to_json())
        installation = self.__collection_client.remove(query_model_json)

        return installation

    def __convert_to_query(self, query_model):
        return self.__convert_helper(query_model, ".")

    def __convert_to_query_value(self, new_values_model):
        return self.__convert_helper(new_values_model, ".$.")

    def __convert_helper(self, model, string_between_key_values):
        model_without_none = self.__remove_none_fields(model)

        model_json = {}
        for key, value in model_without_none.items():
            if isinstance(value, list):
                for list_key, list_value in value[0].items():
                    model_json[key + string_between_key_values + list_key] = list_value
            else:
                model_json[key] = value

        return model_json

    def __remove_none_fields(self, dict):
        return {k: v for k, v in dict.items() if v is not None}

    def __find(self, query):
        return self.__collection_client.find(query)

    def __find_one(self, query):
        return self.__collection_client.find_one(query)

    def __insert_one(self, new_values):
        return self.__collection_client.insert_one(new_values)

    def __upsert(self, query, new_values):
        return self.__collection_client.update_one(query, new_values, upsert=True)

    def __update_one(self, query, new_values):
        return self.__collection_client.update_one(query, new_values)
