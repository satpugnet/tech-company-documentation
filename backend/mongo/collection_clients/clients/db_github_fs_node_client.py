from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.constants.db_update_actions import DbUpdateActions
from mongo.models.db_github_fs_node_model import DbGithubFSNodeModel
from utils.path_manipulator import PathManipulator


class DbGithubFSNodeClient(AbstractDbCollectionClient):
    """
    A client for the github file counter collection.
    """

    def __init__(self):
        super().__init__('github_fs_node', DbGithubFSNodeModel)

    def find_one(self, github_account_login, repo_name, full_path):
        split_path = PathManipulator().dissociate_dir_path_from_fs_node_name(full_path)

        return self._find_one(
            DbGithubFSNodeModel(
                github_account_login=github_account_login,
                repo_name=repo_name,
                dir_path=split_path.dir_path,
                fs_node_name=split_path.fs_node_name
            )
        )

    def insert_one(self, github_account_login, repo_name, dir_path, fs_node_name, type, content):
        return self._insert_one(
                    DbGithubFSNodeModel(
                        github_account_login=github_account_login,
                        repo_name=repo_name,
                        dir_path=dir_path,
                        fs_node_name=fs_node_name,
                        type=type,
                        content=content
                    )
                )

    def update_one(self, github_account_login, repo_name, dir_path, fs_node_name, type, content):
        return self._update_one(
            DbGithubFSNodeModel(
                github_account_login=github_account_login,
                repo_name=repo_name,
                dir_path=dir_path,
                fs_node_name=fs_node_name
            ),
            DbGithubFSNodeModel(
                github_account_login=github_account_login,
                repo_name=repo_name,
                dir_path=dir_path,
                fs_node_name=fs_node_name,
                type=type,
                content=content
            ),
            DbUpdateActions.SET_ACTION
        )

    def remove(self, github_account_login):
        return self._remove(
            DbGithubFSNodeModel(
                github_account_login=github_account_login
            )
        )
