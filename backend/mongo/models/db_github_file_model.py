from mongo.constants.db_fields import DbFields
from utils.json.jsonable import Jsonable


class DbGithubFileModel(Jsonable):
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
            DbFields.GITHUB_ACCOUNT_LOGIN_FIELD: self.__github_account_login,
            DbFields.REPO_NAME_FIELD: self.__repo_name,
            DbFields.DIR_PATH_FIELD: self.__dir_path,
            DbFields.FILENAME_FIELD: self.__filename,
            DbFields.TYPE_FIELD: self.__type,
            DbFields.CONTENT_FIELD: self.__content
        }

    @staticmethod
    def from_json(github_file):
        return DbGithubFileModel(
            github_file[DbFields.GITHUB_ACCOUNT_LOGIN_FIELD],
            github_file[DbFields.REPO_NAME_FIELD],
            github_file[DbFields.DIR_PATH_FIELD],
            github_file[DbFields.FILENAME_FIELD],
            github_file[DbFields.TYPE_FIELD],
            github_file[DbFields.CONTENT_FIELD]
        )
