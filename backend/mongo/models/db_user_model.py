from mongo.constants.model_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


class DbUserModel(AbstractDbCollectionModel):
    """
    Represents a user
    """

    LOGIN_FIELD = ModelFields.LOGIN
    TOKEN_FIELD = ModelFields.TOKEN

    def __init__(self, login=None, token=None):
        self.__login = login
        self.__token = token

    @property
    def login(self):
        return self.__login

    @property
    def token(self):
        return self.__token

    def to_json(self):
        return {
            DbUserModel.LOGIN_FIELD: self.login,
            DbUserModel.TOKEN_FIELD: self.token
        }

    @staticmethod
    def from_json(user):
        return DbUserModel(
            user[DbUserModel.LOGIN_FIELD],
            user[DbUserModel.TOKEN_FIELD]
        )
