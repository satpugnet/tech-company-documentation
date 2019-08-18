from mongo.mongo_client_connection import MongoClientConnection
from utils.json.jsonable import Jsonable


class DbDocumentModel(Jsonable):
    """
    Represents a file of documentation, which will contain reference to code lines
    """

    class FileReferenceModel(Jsonable):
        """
        A FileReferenceModel is part of a Document, and references lines of code in repositories
        """

        def __init__(self, ref_id=None, github_account_login=None, repo_name=None, path=None, start_line=None, end_line=None, is_deleted=None):
            self.__ref_id = ref_id
            self.__github_account_login = github_account_login
            self.__repo_name = repo_name
            self.__path = path
            self.__start_line = start_line
            self.__end_line = end_line
            self.__is_deleted = is_deleted

        @property
        def ref_id(self):
            return self.__ref_id

        @property
        def github_account_login(self):
            return self.__github_account_login

        @property
        def repo_name(self):
            return self.__repo_name

        @property
        def path(self):
            return self.__path

        @property
        def start_line(self):
            return self.__start_line

        @property
        def end_line(self):
            return self.__end_line

        @property
        def is_deleted(self):
            return self.__is_deleted

        def to_json(self):
            return {
                'ref_id': self.ref_id,
                'github_account_login': self.github_account_login,
                'repo_name': self.repo_name,
                'path': self.path,
                'start_line': self.start_line,
                'end_line': self.end_line,
                'is_deleted': self.is_deleted
            }

        @staticmethod
        def from_json(file_ref):
            return DbDocumentModel.FileReferenceModel(
                file_ref['ref_id'],
                file_ref['github_account_login'],
                file_ref['repo_name'],
                file_ref['path'],
                int(file_ref['start_line']),
                int(file_ref['end_line']),
                file_ref['is_deleted']
            )

    def __init__(self, github_account_login=None, name=None, content=None, refs=None):
        self.__github_account_login = github_account_login
        self.__name = name
        self.__content = content
        self.__refs = refs

    @property
    def github_account_login(self):
        return self.__github_account_login

    @property
    def name(self):
        return self.__name

    @property
    def content(self):
        return self.__content

    @property
    def refs(self):
        return self.__refs

    def to_json(self):
        return {
            'github_account_login': self.github_account_login,
            'name': self.name,
            'content': self.content,
            'refs': [ref.to_json() for ref in self.refs] if self.refs is not None else None,
        }

    @staticmethod
    def from_json(document):
        return DbDocumentModel(
            document['github_account_login'],
            document['name'],
            document['content'],
            [DbDocumentModel.FileReferenceModel.from_json(ref) for ref in document['refs']]
        )
