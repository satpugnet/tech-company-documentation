from mongo.constants.model_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


class DbGithubFSNodeModel(AbstractDbCollectionModel):
    """
    Represents a file in github.
    """

    GITHUB_ACCOUNT_LOGIN_FIELD = ModelFields.GITHUB_ACCOUNT_LOGIN
    REPO_NAME_FIELD = ModelFields.REPO_NAME
    DIR_PATH_FIELD = ModelFields.DIR_PATH
    FS_NODE_NAME_FIELD = ModelFields.FS_NODE_NAME
    TYPE_FIELD = ModelFields.TYPE
    CONTENT_FIELD = ModelFields.CONTENT

    def __init__(self, github_account_login=None, repo_name=None, dir_path=None, fs_node_name=None, type=None, content=None):
        self.__github_account_login = github_account_login
        self.__repo_name = repo_name
        self.__dir_path = dir_path
        self.__fs_node_name = fs_node_name
        self.__type = type
        self.__content = content

    @property
    def github_account_login(self):
        return self.__github_account_login

    @property
    def repo_name(self):
        return self.__repo_name

    @property
    def dir_path(self):
        return self.__dir_path

    @property
    def fs_node_name(self):
        return self.__fs_node_name

    @property
    def type(self):
        return self.__type

    @property
    def content(self):
        return self.__content

    def to_json(self):
        return {
            DbGithubFSNodeModel.GITHUB_ACCOUNT_LOGIN_FIELD: self.__github_account_login,
            DbGithubFSNodeModel.REPO_NAME_FIELD: self.__repo_name,
            DbGithubFSNodeModel.DIR_PATH_FIELD: self.__dir_path,
            DbGithubFSNodeModel.FS_NODE_NAME_FIELD: self.__fs_node_name,
            DbGithubFSNodeModel.TYPE_FIELD: self.__type,
            DbGithubFSNodeModel.CONTENT_FIELD: self.__content
        }

    @staticmethod
    def from_json(github_file):
        return DbGithubFSNodeModel(
            github_file[DbGithubFSNodeModel.GITHUB_ACCOUNT_LOGIN_FIELD],
            github_file[DbGithubFSNodeModel.REPO_NAME_FIELD],
            github_file[DbGithubFSNodeModel.DIR_PATH_FIELD],
            github_file[DbGithubFSNodeModel.FS_NODE_NAME_FIELD],
            github_file[DbGithubFSNodeModel.TYPE_FIELD],
            github_file[DbGithubFSNodeModel.CONTENT_FIELD]
        )
