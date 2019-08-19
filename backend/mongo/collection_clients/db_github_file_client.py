from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.models.db_github_file_model import DbGithubFileModel


class DbGithubFileClient(AbstractDbCollectionClient):
    """
    Represents a file in github
    """

    def __init__(self):
        super().__init__('github_file', DbGithubFileModel)

    def find_one(self, github_account_login, repo_name, dir_path, filename):
        return self._find_one(
            DbGithubFileModel(
                github_account_login=github_account_login,
                repo_name=repo_name,
                dir_path=dir_path,
                filename=filename
            )
        )

    def upsert(self, github_account_login, repo_name, dir_path, filename, type, content):
        return self._upsert(
            DbGithubFileModel(
                github_account_login=github_account_login,
                repo_name=repo_name,
                dir_path=dir_path,
                filename=filename
            ),
            DbGithubFileModel(
                github_account_login=github_account_login,
                repo_name=repo_name,
                dir_path=dir_path,
                filename=filename,
                type=type,
                content=content
            )
        )

    def remove(self, github_account_login):
        return self._remove(
            DbGithubFileModel(
                github_account_login=github_account_login
            )
        )
