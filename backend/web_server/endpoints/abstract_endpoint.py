from flask import jsonify, request
from flask_restful import Resource


class AbstractEndpoint(Resource):

    COOKIE_USER_LOGIN_FIELD = 'user_login'

    def __init__(self):
        self._get_output_schema_instance = None
        self._post_output_schema_instance = None
        self._put_output_schema_instance = None
        self._patch_output_schema_instance = None
        self._delete_output_schema_instance = None

    def _create_validated_response(self, json_or_object):
        response = {}

        if self._get_output_schema_instance and request.method == "GET":
            response = self._get_output_schema_instance.dump(json_or_object)
        elif self._post_output_schema_instance and request.method == "POST":
            response = self._post_output_schema_instance.dump(json_or_object)
        elif self._put_output_schema_instance and request.method == "PUT":
            response = self._put_output_schema_instance.dump(json_or_object)
        elif self._patch_output_schema_instance and request.method == "PATCH":
            response = self._patch_output_schema_instance.dump(json_or_object)
        elif self._delete_output_schema_instance and request.method == "DELETE":
            response = self._delete_output_schema_instance.dump(json_or_object)

        return jsonify(response)

    def _create_empty_response(self):
        return jsonify({})
