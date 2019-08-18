from mongo.mongo_client import DB


class Repository:
    """
    Represents a github repository, used to keep track of the state of the internal db for this repository
    """

    COLLECTION = DB['repository']  # Reference to the mongo collection

    REPOSITORY_FULL_NAME_FIELD = "repository_full_name"
    SHA_LAST_UPDATE_FIELD = "sha_last_update"

    def __init__(self, repository_full_name, sha_last_update):
        self.repository_full_name = repository_full_name
        self.sha_last_update = sha_last_update

    def insert(self):
        return self.COLLECTION.insert_one(self.to_json())

    @staticmethod
    def __upsert(query, new_values):
        return Repository.COLLECTION.update_one(query, new_values, upsert=True)

    @staticmethod
    def upsert_sha_last_update(repository_full_name, sha_last_update):
        query = {
            Repository.REPOSITORY_FULL_NAME_FIELD: repository_full_name
        }

        new_values = {
            "$set": {
                Repository.SHA_LAST_UPDATE_FIELD: sha_last_update
            }
        }

        return Repository.__upsert(query, new_values)

    @staticmethod
    def find(repository_full_name):
        doc = Repository.COLLECTION.find_one({
            Repository.REPOSITORY_FULL_NAME_FIELD: repository_full_name
        })

        if not doc:
            return None

        return Repository.from_json(doc)

    def to_json(self):
        return {
            Repository.REPOSITORY_FULL_NAME_FIELD: self.repository_full_name,
            Repository.SHA_LAST_UPDATE_FIELD: self.sha_last_update
        }

    @staticmethod
    def from_json(repository):
        return Repository(
            repository[Repository.REPOSITORY_FULL_NAME_FIELD],
            repository[Repository.SHA_LAST_UPDATE_FIELD]
        )