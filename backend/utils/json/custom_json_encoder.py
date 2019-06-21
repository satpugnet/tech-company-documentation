import json

from utils.json.jsonable import Jsonable


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Jsonable):
            return obj.to_json()

        return json.JSONEncoder.default(self, obj)

