from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.constants.db_update_actions import DbUpdateActions
from mongo.models.db_github_file_model import DbGithubFileModel


class DbGithubFileClient(AbstractDbCollectionClient):
    """
    A client for the github file counter collection.
    """

    def __init__(self):
        super().__init__('github_file', DbGithubFileModel)

    def insert_one(self, github_account_login, repo_name, dir_path, filename, type, content):
        return self._insert_one(
                    DbGithubFileModel(
                        github_account_login=github_account_login,
                        repo_name=repo_name,
                        dir_path=dir_path,
                        filename=filename,
                        type=type,
                        content=content
                    )
                )

    def update_one(self, github_account_login, repo_name, dir_path, filename, type, content):
        return self._update_one(
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
            ),
            DbUpdateActions.SET_ACTION
        )

    def remove(self, github_account_login):
        return self._remove(
            DbGithubFileModel(
                github_account_login=github_account_login
            )
        )
