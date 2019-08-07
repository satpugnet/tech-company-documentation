from datetime import datetime, timezone

from github_interface.authorisation_interface import GithubAuthorisationInterface
from mongo.mongo_client import DB
from utils.file_interface import FileInterface


class Installation:
    """
    Represents an installation
    """

    COLLECTION = DB['installation']  # Reference to the mongo collection

    def __init__(self, account_login, installation_id, installation_token, expires_at):
        self.account_login = account_login
        self.installation_id = installation_id
        self.installation_token = installation_token # Anytime this is accessed, the expires_at must be checked
        self.expires_at = expires_at

    def insert(self):
        return self.COLLECTION.insert_one(self.to_json())

    @staticmethod
    def __upsert(query, new_values):
        return Installation.COLLECTION.update(query, new_values, upsert=True)

    @staticmethod
    def __upsert_updated_installation(account_login, installation_id):
        installation_token, expires_at = GithubAuthorisationInterface.get_installation_access_token(installation_id, FileInterface.load_private_key())
        query = {"account_login": account_login}
        new_values = {
            "$set": {
                "account_login": account_login,
                "installation_id": installation_id,
                "installation_token": installation_token,
                "expires_at": expires_at
            }
        }

        return Installation.__upsert(query, new_values)

    @staticmethod
    def __find(account_login):
        installation = Installation.COLLECTION.find_one({
            'account_login': account_login
        })
        
        return installation

    @staticmethod
    def find(account_login):
        installation = Installation.__find(account_login)

        if not installation:
            return None

        installation_object = Installation.from_json(installation)

        if Installation.__is_expired(installation_object):
            Installation.__upsert_updated_installation(account_login, installation_object.installation_id)
            installation = Installation.__find(account_login)
            return Installation.from_json(installation)
        else:
            return installation_object

    @staticmethod
    def insert_if_not_exist(account_login, installation_id):
        if Installation.find(account_login) is not None:
            return

        Installation.__upsert_updated_installation(account_login, installation_id)

    @staticmethod
    def __is_expired(installation_object):
        return installation_object.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc)

    def to_json(self):
        return {
            'account_login': self.account_login,
            'installation_id': self.installation_id,
            'installation_token': self.installation_token,
            'expires_at': self.expires_at
        }

    @staticmethod
    def from_json(installation):
        return Installation(
            installation['account_login'],
            installation['installation_id'],
            installation['installation_token'],
            installation['expires_at']
        )
