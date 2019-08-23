from abc import ABC

from tools.json.jsonable import Jsonable


class AbstractDbCollectionModel(Jsonable, ABC):

    DOT_SIGN = "."
    DOT_DOLLAR_DOT_SIGN = ".$."
    DOLLAR_SIGN = "$"

    def to_db_json_filter_query(self):
        json_without_none = self.__remove_none_fields(self.to_json())

        return self.__transform_list_values(json_without_none, AbstractDbCollectionModel.DOT_SIGN)

    def to_db_json_update_query(self, update_action):
        key = AbstractDbCollectionModel.DOLLAR_SIGN + str(update_action)
        json_without_none = self.__remove_none_fields(self.to_json())
        value = self.__transform_list_values(json_without_none, AbstractDbCollectionModel.DOT_DOLLAR_DOT_SIGN)

        return {key: value}

    def to_db_json_insert_query(self):
        return self.__remove_none_fields(self.to_json())

    def __remove_none_fields(self, dict):
        return {k: v for k, v in dict.items() if v is not None}

    def __transform_list_values(self, model, string_between_key_values):
        model_json = {}

        for key, value in model.items():

            if isinstance(value, list):
                for list_key, list_value in value[0].items():
                    model_json[key + string_between_key_values + list_key] = list_value

            else:
                model_json[key] = value

        return model_json
