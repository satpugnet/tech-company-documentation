from mongo.mongo_client_connection import MongoClientConnection
from utils.json.jsonable import Jsonable


class DbUserModel(Jsonable):
    """
    Represents a user
    """

    COLLECTION = MongoClientConnection.DB['user']

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
            'login': self.login,
            'user_token': self.user_token
        }

    @staticmethod
    def from_json(user):
        return DbUserModel(
            user['login'],
            user['user_token']
        )
