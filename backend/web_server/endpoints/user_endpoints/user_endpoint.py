from flask import session
from marshmallow import Schema, fields

from mongo.constants.model_fields import ModelFields
from web_server.endpoints.abstract_endpoint import AbstractEndpoint
from web_server.endpoints.user_endpoints.abstract_user_endpoint import AbstractUserEndpoint


class UserEndpoint(AbstractUserEndpoint):

    def __init__(self):
        super().__init__()
        self._get_output_schema_instance = Schema.from_dict({
            ModelFields.USER_LOGIN: fields.Str(required=True)
        })()

    def get(self):

        return self._create_validated_response({
            ModelFields.USER_LOGIN: session[AbstractEndpoint.COOKIE_USER_LOGIN_FIELD]
        })
