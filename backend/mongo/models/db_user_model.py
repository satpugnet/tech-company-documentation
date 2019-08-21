from mongo.constants.db_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


class DbUserModel(AbstractDbCollectionModel):
    """
    Represents a user
    """

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
            ModelFields.LOGIN: self.login,
            ModelFields.TOKEN: self.token
        }

    @staticmethod
    def from_json(user):
        return DbUserModel(
            user[ModelFields.LOGIN],
            user[ModelFields.TOKEN]
        )
