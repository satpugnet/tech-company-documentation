from mongo.mongo_client import DB


class DbRepo:
    """
    Represents a github repository, used to keep track of the state of the internal db for this repository
    """

    COLLECTION = DB['repo']  # Reference to the mongo collection

    def __init__(self, org_user_account, repo, sha_last_update):
        self.org_user_account = org_user_account
        self.repo = repo
        self.sha_last_update = sha_last_update

    def insert(self):
        return self.COLLECTION.insert_one(self.to_json())

    @staticmethod
    def __upsert(query, new_values):
        return DbRepo.COLLECTION.update_one(query, new_values, upsert=True)

    @staticmethod
    def upsert(org_user_account, repo):
        query = {
            "org_user_account": org_user_account,
            "repo": repo
        }
        new_values = {
            "$set": {
                "org_user_account": org_user_account,
                "repo": repo,
                "sha_last_update": ""
            }
        }

        return DbRepo.__upsert(query, new_values)

    @staticmethod
    def upsert_sha_last_update(org_user_account, repo, sha_last_update):
        query = {
            "org_user_account": org_user_account,
            "repo": repo
        }
        new_values = {
            "$set": {
                "sha_last_update": sha_last_update
            }
        }

        return DbRepo.__upsert(query, new_values)

    @staticmethod
    def find(repo):
        doc = DbRepo.COLLECTION.find_one({
            'repo': repo
        })

        if not doc:
            return None

        return DbRepo.from_json(doc)

    @staticmethod
    def remove(org_user_account):
        installation = DbRepo.COLLECTION.remove({
            'org_user_account': org_user_account
        })

        return installation

    def to_json(self):
        return {
            'org_user_account': self.org_user_account,
            'repo': self.repo,
            'sha_last_update': self.sha_last_update
        }

    @staticmethod
    def from_json(repository):
        return DbRepo(
            repository['org_user_account'],
            repository['repo'],
            repository['sha_last_update']
        )
