from mongo.mongo_client import DB


class DbGithubFile:
    """
    Represents a file in github
    """

    COLLECTION = DB['github_file']  # Reference to the mongo collection

    def __init__(self, org_user_account, repo, dir_path, filename, type, content):
        self.org_user_account = org_user_account,
        self.repo = repo
        self.dir_path = dir_path
        self.filename = filename
        self.type = type
        self.content = content

    def insert(self):
        return self.COLLECTION.insert_one(self.to_json())

    @staticmethod
    def __upsert(query, new_values):
        return DbGithubFile.COLLECTION.update_one(query, new_values, upsert=True)

    @staticmethod
    def upsert(org_user_account, repo, dir_path, filename, type, content):
        query = {
            "org_user_account": org_user_account,
            "repo": repo,
            "dir_path": dir_path,
            "filename": filename
        }
        new_values = {
            "$set": {
                "org_user_account": org_user_account,
                "repo": repo,
                "dir_path": dir_path,
                "filename": filename,
                "type": type,
                "content": content
            }
        }

        return DbGithubFile.__upsert(query, new_values)

    @staticmethod
    def find(org_user_account, repo, dir_path, filename):
        github_file = DbGithubFile.COLLECTION.find_one({
            "org_user_account": org_user_account,
            "repo": repo,
            "dir_path": dir_path,
            "filename": filename
        })

        if not github_file:
            return None

        return DbGithubFile.from_json(github_file)

    @staticmethod
    def remove(org_user_account):
        installation = DbGithubFile.COLLECTION.remove({
            'org_user_account': org_user_account
        })

        return installation

    def to_json(self):
        return {
            'org_user_account': self.org_user_account,
            'repo': self.repo,
            'dir_path': self.dir_path,
            'filename': self.filename,
            'type': self.type,
            'content': self.content
        }

    @staticmethod
    def from_json(github_file):
        return DbGithubFile(
            github_file['org_user_account'],
            github_file['repo'],
            github_file['dir_path'],
            github_file['filename'],
            github_file['type'],
            github_file['content']
        )
