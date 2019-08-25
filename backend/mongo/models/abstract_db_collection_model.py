from abc import ABC

from tools.json.jsonable import Jsonable


class AbstractDbCollectionModel(Jsonable, ABC):
    """
    Abstract collection model.
    """

    DOT_SIGN = "."
    DOT_DOLLAR_DOT_SIGN = ".$."
    DOLLAR_SIGN = "$"

    def to_db_json_filter_query(self):
        """
        :return: A formatted mongodb filter query using the model data.
        """

        json_without_none = self.__remove_none_values(self.to_json())

        return self.__transform_list_values(json_without_none, AbstractDbCollectionModel.DOT_SIGN)

    def to_db_json_update_query(self, update_action):
        """
        :return: A formatted mongodb update query using the model data.
        """

        key = AbstractDbCollectionModel.DOLLAR_SIGN + str(update_action)
        json_without_none = self.__remove_none_values(self.to_json())
        value = self.__transform_list_values(json_without_none, AbstractDbCollectionModel.DOT_DOLLAR_DOT_SIGN)

        return {key: value}

    def to_db_json_insert_query(self):
        """
        :return: A formatted mongodb insert query using the model data.
        """
        return self.__remove_none_values(self.to_json())

    def __remove_none_values(self, d):
        """
        :return: A dictionary with None values.
        """
        if not isinstance(d, (dict, list)):
            return d
        if isinstance(d, list):
            return [v for v in (self.__remove_none_values(v) for v in d) if v is not None]
        return {k: v for k, v in ((k, self.__remove_none_values(v)) for k, v in d.items()) if v is not None}

    def __transform_list_values(self, model, string_between_key_values):
        """
        :return: A formatted dictionary where the list values are formatter using the string_between_key_values input.
        The rest of the dictionary is unchanged.
        """

        model_json = {}

        for key, value in model.items():

            if isinstance(value, list):
                for list_key, list_value in value[0].items():
                    model_json[key + string_between_key_values + list_key] = list_value

            else:
                model_json[key] = value

        return model_json
