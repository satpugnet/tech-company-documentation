from marshmallow import Schema, fields, post_load, EXCLUDE

from mongo.constants.model_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


class DbUserModel(AbstractDbCollectionModel):
    """
    Represents a user
    """

    LOGIN_FIELD = ModelFields.LOGIN
    TOKEN_FIELD = ModelFields.TOKEN

    class DbUserSchema(Schema):
        login = fields.Str(required=True)
        token = fields.Str(required=True)

        @post_load
        def make_user(self, data, **kwargs):
            return DbUserModel(**data)

    schema_class = DbUserSchema

    def __init__(self, login=None, token=None):
        self.__login = login
        self.__token = token

    @property
    def login(self):
        return self.__login

    @property
    def token(self):
        return self.__token
