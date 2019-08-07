from mongo.mongo_client import DB


class User:
    """
    Represents a user
    """

    COLLECTION = DB['user']  # Reference to the mongo collection

    def __init__(self, login, user_token):
        self.login = login
        self.user_token = user_token

    def insert(self):
        return self.COLLECTION.insert_one(self.to_json())

    @staticmethod
    def __upsert(query, new_values):
        return User.COLLECTION.update(query, new_values, upsert=True)

    @staticmethod
    def __update(query, new_values):
        return User.COLLECTION.update(query, new_values)

    @staticmethod
    def upsert_user_token(login, user_token):
        query = {"login": login}
        new_values = {
            "$set": {
                "user_token": user_token
            }
        }

        return User.__upsert(query, new_values)

    @staticmethod
    def find_all():
        users = User.COLLECTION.find({})

        return [User.from_json(user) for user in users]

    @staticmethod
    def find(user_login):
        user = User.COLLECTION.find_one({
            'login': user_login
        })

        if not user:
            return None

        return User.from_json(user)

    def to_json(self):
        return {
            'login': self.login,
            'user_token': self.user_token
        }

    @staticmethod
    def from_json(user):
        return User(
            user['login'],
            user['user_token']
        )
