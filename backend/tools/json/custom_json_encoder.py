import json

from tools.json.jsonable import Jsonable


class CustomJsonEncoder(json.JSONEncoder):
    """
    A custom json encoder used by flask to jsonify.
    @deprecated as we are now using the marshmallow library for the json conversion.
    """

    def default(self, obj):

        if isinstance(obj, Jsonable):
            return obj.to_json()

        return json.JSONEncoder.default(self, obj)

