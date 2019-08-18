from datetime import datetime, timezone

from github_interface.authorisation_interface import GithubAuthorisationInterface
from mongo.models.counter import Counter
from mongo.mongo_client import DB
from tools import logger
from utils.file_interface import FileInterface


class AccountInstallation:
    """
    Represents an account installation
    """

    COLLECTION = DB['account_installation']  # Reference to the mongo collection

    MONGO_ID_FIELD = "_id"
    ACCOUNT_LOGIN_FIELD = "account_login"
    INSTALLATION_ID_FIELD = "installation_id"
    INSTALLATION_TOKEN_FIELD = "installation_token"
    EXPIRES_AT_FIELD = "expires_at"

    def __init__(self, mongo_id, account_login, installation_id, installation_token, expires_at):
        self.mongo_id = mongo_id
        self.account_login = account_login
        self.installation_id = installation_id
        self.installation_token = installation_token  # Anytime this is accessed, the expires_at must be checked
        self.expires_at = expires_at

    @staticmethod
    def insert(account_login, installation_id):
        installation_token, expires_at = GithubAuthorisationInterface.get_installation_access_token(
            installation_id,
            FileInterface.load_private_key()
        )

        mongo_id = Counter.get_next_account_installation_id()

        account_installation = AccountInstallation(
            mongo_id,
            account_login,
            installation_id,
            installation_token,
            expires_at
        )

        logger.get_logger().info("Inserting account %s with id %s", account_login, mongo_id)

        try:
            AccountInstallation.COLLECTION.insert(account_installation.to_json())
            logger.get_logger().info("Successfully inserted account %s with id %s", account_login, mongo_id)
        except Exception:
            logger.get_logger().error("Failed to insert account %s with id %s", account_login, mongo_id)

    @staticmethod
    def update_installation_token(mongo_id, installation_id):
        installation_token, expires_at = GithubAuthorisationInterface.get_installation_access_token(
            installation_id,
            FileInterface.load_private_key()
        )

        query = {
            AccountInstallation.MONGO_ID_FIELD: mongo_id
        }

        new_values = {
            "$set": {
                AccountInstallation.INSTALLATION_TOKEN_FIELD: installation_token,
                AccountInstallation.EXPIRES_AT_FIELD: expires_at
            }
        }

        return AccountInstallation.COLLECTION.update(query, new_values)

    @staticmethod
    def __find(account_login):
        installation = AccountInstallation.COLLECTION.find_one({
            AccountInstallation.ACCOUNT_LOGIN_FIELD: account_login
        })

        return installation

    @staticmethod
    def find(account_login):
        installation = AccountInstallation.__find(account_login)

        if not installation:
            return None

        installation_object = AccountInstallation.from_json(installation)

        if AccountInstallation.__is_expired(installation_object):
            AccountInstallation.update_installation_token(installation_object.mongo_id, installation_object.installation_id)
            installation = AccountInstallation.__find(account_login)
            return AccountInstallation.from_json(installation)

        else:
            return installation_object

    @staticmethod
    def insert_if_not_exist(account_login, installation_id):
        if AccountInstallation.find(account_login) is not None:
            return

        AccountInstallation.insert(account_login, installation_id)

    @staticmethod
    def remove(account_login):
        installation = AccountInstallation.COLLECTION.remove({
            AccountInstallation.ACCOUNT_LOGIN_FIELD: account_login
        })

        return installation

    @staticmethod
    def __is_expired(installation_object):
        return installation_object.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc)

    def to_json(self):
        return {
            AccountInstallation.MONGO_ID_FIELD: self.mongo_id,
            AccountInstallation.ACCOUNT_LOGIN_FIELD: self.account_login,
            AccountInstallation.INSTALLATION_ID_FIELD: self.installation_id,
            AccountInstallation.INSTALLATION_TOKEN_FIELD: self.installation_token,
            AccountInstallation.EXPIRES_AT_FIELD: self.expires_at
        }

    @staticmethod
    def from_json(installation):
        return AccountInstallation(
            installation[AccountInstallation.MONGO_ID_FIELD],
            installation[AccountInstallation.ACCOUNT_LOGIN_FIELD],
            installation[AccountInstallation.INSTALLATION_ID_FIELD],
            installation[AccountInstallation.INSTALLATION_TOKEN_FIELD],
            installation[AccountInstallation.EXPIRES_AT_FIELD]
        )
