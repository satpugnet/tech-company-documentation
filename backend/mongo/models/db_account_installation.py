from datetime import datetime, timezone

from github_interface.authorisation_interface import GithubAuthorisationInterface
from mongo.mongo_client import DB
from utils.file_interface import FileInterface


class DbAccountInstallation:
    """
    Represents an account installation
    """

    COLLECTION = DB['account_installation']  # Reference to the mongo collection

    def __init__(self, org_user_account, installation_id, installation_token, expires_at):
        self.org_user_account = org_user_account
        self.installation_id = installation_id
        self.installation_token = installation_token # Anytime this is accessed, the expires_at must be checked
        self.expires_at = expires_at

    def insert(self):
        return self.COLLECTION.insert_one(self.to_json())

    @staticmethod
    def __upsert(query, new_values):
        return DbAccountInstallation.COLLECTION.update(query, new_values, upsert=True)

    @staticmethod
    def __upsert_updated_installation(org_user_account, installation_id):
        installation_token, expires_at = GithubAuthorisationInterface.get_installation_access_token(installation_id, FileInterface.load_private_key())
        query = {"org_user_account": org_user_account}
        new_values = {
            "$set": {
                "org_user_account": org_user_account,
                "installation_id": installation_id,
                "installation_token": installation_token,
                "expires_at": expires_at
            }
        }

        return DbAccountInstallation.__upsert(query, new_values)

    @staticmethod
    def __find(org_user_account):
        installation = DbAccountInstallation.COLLECTION.find_one({
            'org_user_account': org_user_account
        })
        
        return installation

    @staticmethod
    def find(org_user_account):
        installation = DbAccountInstallation.__find(org_user_account)

        if not installation:
            return None

        installation_object = DbAccountInstallation.from_json(installation)

        if DbAccountInstallation.__is_expired(installation_object):
            DbAccountInstallation.__upsert_updated_installation(org_user_account, installation_object.installation_id)
            installation = DbAccountInstallation.__find(org_user_account)
            return DbAccountInstallation.from_json(installation)
        else:
            return installation_object

    @staticmethod
    def insert_if_not_exist(org_user_account, installation_id):
        if DbAccountInstallation.find(org_user_account) is not None:
            return

        DbAccountInstallation.__upsert_updated_installation(org_user_account, installation_id)

    @staticmethod
    def remove(org_user_account):
        installation = DbAccountInstallation.COLLECTION.remove({
            'org_user_account': org_user_account
        })

        return installation

    @staticmethod
    def __is_expired(installation_object):
        return installation_object.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc)

    def to_json(self):
        return {
            'org_user_account': self.org_user_account,
            'installation_id': self.installation_id,
            'installation_token': self.installation_token,
            'expires_at': self.expires_at
        }

    @staticmethod
    def from_json(installation):
        return DbAccountInstallation(
            installation['org_user_account'],
            installation['installation_id'],
            installation['installation_token'],
            installation['expires_at']
        )
