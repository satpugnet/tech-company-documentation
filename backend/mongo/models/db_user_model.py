from mongo.constants.db_fields import DbFields
from utils.json.jsonable import Jsonable


class DbUserModel(Jsonable):
    """
    Represents a user
    """

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
            DbFields.LOGIN_FIELD: self.login,
            DbFields.USER_TOKEN_FIELD: self.user_token
        }

    @staticmethod
    def from_json(user):
        return DbUserModel(
            user[DbFields.LOGIN_FIELD],
            user[DbFields.USER_TOKEN_FIELD]
        )
