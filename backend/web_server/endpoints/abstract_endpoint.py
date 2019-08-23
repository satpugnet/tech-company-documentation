from flask import jsonify
from flask_restful import Resource


# TODO: add patch ?
class AbstractEndpoint(Resource):

    USER_LOGIN_FIELD = 'user_login'

    def _create_response(self, json):
        return jsonify(json)
