from mongo.constants.model_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


class DbGithubFileModel(AbstractDbCollectionModel):
    """
    Represents a file in github.
    """

    GITHUB_ACCOUNT_LOGIN_FIELD = ModelFields.GITHUB_ACCOUNT_LOGIN
    REPO_NAME_FIELD = ModelFields.REPO_NAME
    DIR_PATH_FIELD = ModelFields.DIR_PATH
    FILENAME_FIELD = ModelFields.FILENAME
    TYPE_FIELD = ModelFields.TYPE
    CONTENT_FIELD = ModelFields.CONTENT

    def __init__(self, github_account_login=None, repo_name=None, dir_path=None, filename=None, type=None, content=None):
        self.__github_account_login = github_account_login
        self.__repo_name = repo_name
        self.__dir_path = dir_path
        self.__filename = filename
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
    def filename(self):
        return self.__filename

    @property
    def type(self):
        return self.__type

    @property
    def content(self):
        return self.__content

    def to_json(self):
        return {
            DbGithubFileModel.GITHUB_ACCOUNT_LOGIN_FIELD: self.__github_account_login,
            DbGithubFileModel.REPO_NAME_FIELD: self.__repo_name,
            DbGithubFileModel.DIR_PATH_FIELD: self.__dir_path,
            DbGithubFileModel.FILENAME_FIELD: self.__filename,
            DbGithubFileModel.TYPE_FIELD: self.__type,
            DbGithubFileModel.CONTENT_FIELD: self.__content
        }

    @staticmethod
    def from_json(github_file):
        return DbGithubFileModel(
            github_file[DbGithubFileModel.GITHUB_ACCOUNT_LOGIN_FIELD],
            github_file[DbGithubFileModel.REPO_NAME_FIELD],
            github_file[DbGithubFileModel.DIR_PATH_FIELD],
            github_file[DbGithubFileModel.FILENAME_FIELD],
            github_file[DbGithubFileModel.TYPE_FIELD],
            github_file[DbGithubFileModel.CONTENT_FIELD]
        )
