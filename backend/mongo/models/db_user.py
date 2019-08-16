from mongo.mongo_client import DB


class DbUser:
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
        return DbUser.COLLECTION.update(query, new_values, upsert=True)

    @staticmethod
    def __update(query, new_values):
        return DbUser.COLLECTION.update(query, new_values)

    @staticmethod
    def upsert_user_token(login, user_token):
        query = {"login": login}
        new_values = {
            "$set": {
                "user_token": user_token
            }
        }

        return DbUser.__upsert(query, new_values)

    @staticmethod
    def find_all():
        users = DbUser.COLLECTION.find({})

        return [DbUser.from_json(user) for user in users]

    @staticmethod
    def find(user_login):
        user = DbUser.COLLECTION.find_one({
            'login': user_login
        })

        if not user:
            return None

        return DbUser.from_json(user)

    def to_json(self):
        return {
            'login': self.login,
            'user_token': self.user_token
        }

    @staticmethod
    def from_json(user):
        return DbUser(
            user['login'],
            user['user_token']
        )
