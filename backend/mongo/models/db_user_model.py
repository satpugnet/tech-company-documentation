from mongo.mongo_client_connection import MongoClientConnection
from utils.json.jsonable import Jsonable


class DbUserModel(Jsonable):
    """
    Represents a user
    """

    LOGIN_FIELD = "login"
    USER_TOKEN_FIELD = "user_token"

    def __init__(self, login=None, user_token=None):
        self.__login = login
        self.__user_token = user_token

    @property
    def login(self):
        return self.__login

    @property
    def user_token(self):
        return self.__user_token

    def to_json(self):
        return {
            DbUserModel.LOGIN_FIELD: self.login,
            DbUserModel.USER_TOKEN_FIELD: self.user_token
        }

    @staticmethod
    def from_json(user):
        return DbUserModel(
            user[DbUserModel.LOGIN_FIELD],
            user[DbUserModel.USER_TOKEN_FIELD]
        )
