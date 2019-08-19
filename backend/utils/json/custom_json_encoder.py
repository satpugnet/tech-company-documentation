import json

from utils.json.jsonable import Jsonable
from utils.json.sensitive_jsonable import SensitiveJsonable


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SensitiveJsonable):
            return obj.non_sensitive_data_to_json()
        elif isinstance(obj, Jsonable):
            return obj.to_json()

        return json.JSONEncoder.default(self, obj)

