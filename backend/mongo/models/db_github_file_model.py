from mongo.constants.db_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


class DbGithubFileModel(AbstractDbCollectionModel):
    """
    Represents a file in github
    """

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
            ModelFields.GITHUB_ACCOUNT_LOGIN: self.__github_account_login,
            ModelFields.REPO_NAME: self.__repo_name,
            ModelFields.DIR_PATH: self.__dir_path,
            ModelFields.FILENAME: self.__filename,
            ModelFields.TYPE: self.__type,
            ModelFields.CONTENT: self.__content
        }

    @staticmethod
    def from_json(github_file):
        return DbGithubFileModel(
            github_file[ModelFields.GITHUB_ACCOUNT_LOGIN],
            github_file[ModelFields.REPO_NAME],
            github_file[ModelFields.DIR_PATH],
            github_file[ModelFields.FILENAME],
            github_file[ModelFields.TYPE],
            github_file[ModelFields.CONTENT]
        )
