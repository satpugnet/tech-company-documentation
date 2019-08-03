from mongo.mongo_client import DB


class User:
    """
    Represents a user, which will contain reference to code lines
    """

    COLLECTION = DB['user']  # Reference to the mongo collection

    class Installation:
        """
        An Installation is part of a User, and keep track of all installation belonging to a user
        """

        def __init__(self, account_login, installation_token):
            self.account_login = account_login
            self.installation_token = installation_token

        def to_json(self):
            return {
                'account_login': self.account_login,
                'installation_token': self.installation_token
            }

        @staticmethod
        def from_json(file_ref):
            return User.Installation(
                file_ref['account_login'],
                file_ref['installation_token']
            )

    def __init__(self, login, user_token, installations):
        self.login = login
        self.user_token = user_token
        self.installations = installations

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
            },
            "$setOnInsert": {
                "installations": []
            }
        }

        return User.__upsert(query, new_values)

    @staticmethod
    def upsert_installation(user_login, account_login, installation_token):
        # This needs to be implemented in 2 steps to avoid race conditions
        query_push = {"login": user_login, "installations.account_login": { "$ne": account_login }}

        new_values_push = {
            "$push": {
                "installations": {
                    "account_login": account_login,
                    "installation_token": installation_token
                }
            }
        }

        result_push = User.__update(query_push, new_values_push)

        if result_push["n"] == 0:
            query_update = {"login": user_login, "installations.account_login": account_login }

            new_values2_update = {
                "$set": {
                    "installations.$.account_login": account_login,
                    "installations.$.installation_token": installation_token
                }
            }

            User.__update(query_update, new_values2_update)

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

    @staticmethod
    def find_installation(user_login, installation_account_login):
        installation = next(filter(lambda x: x.account_login == installation_account_login, User.find(user_login).installations))
        return installation

    #TODO: Improve this brute-force approach
    @staticmethod
    def find_installation_without_user_authentification(installation_account_login):
        users = User.find_all()

        for user in users:
            current_installation = next(filter(lambda x: x.account_login == installation_account_login, user.installations))
            if current_installation:
                break
        return current_installation

    def to_json(self):
        return {
            'login': self.login,
            'user_token': self.user_token,
            'installations': [installation.to_json() for installation in self.installations]
        }

    @staticmethod
    def from_json(user):
        return User(
            user['login'],
            user['user_token'],
            [User.Installation.from_json(installation) for installation in user['installations']]
        )
