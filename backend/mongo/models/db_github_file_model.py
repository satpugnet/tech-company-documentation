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
            'github_account_login': self.__github_account_login,
            'repo_name': self.__repo_name,
            'dir_path': self.__dir_path,
            'filename': self.__filename,
            'type': self.__type,
            'content': self.__content
        }

    @staticmethod
    def from_json(github_file):
        return DbGithubFileModel(
            github_file['github_account_login'],
            github_file['repo_name'],
            github_file['dir_path'],
            github_file['filename'],
            github_file['type'],
            github_file['content']
        )
