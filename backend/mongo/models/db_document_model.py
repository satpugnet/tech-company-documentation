from mongo.constants.db_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


# TODO: those could be simplify much further using marshmallow library or the **kwargs and a dictionary to create a generic function
from tools.json.jsonable import Jsonable


class DbDocumentModel(AbstractDbCollectionModel):
    """
    Represents a file of documentation, which will contain reference to code lines
    """

    class DbFileReferenceModel(Jsonable):
        """
        A FileReferenceModel is part of a Document, and references lines of code in repositories
        """

        def __init__(self, id=None, github_account_login=None, repo_name=None, path=None, start_line=None, end_line=None, is_deleted=None):
            self.__id = id
            self.__github_account_login = github_account_login
            self.__repo_name = repo_name
            self.__path = path
            self.__start_line = start_line
            self.__end_line = end_line
            self.__is_deleted = is_deleted

        @property
        def id(self):
            return self.__id

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
                ModelFields.ID: self.id,
                ModelFields.GITHUB_ACCOUNT_LOGIN: self.github_account_login,
                ModelFields.REPO_NAME: self.repo_name,
                ModelFields.PATH: self.path,
                ModelFields.START_LINE: self.start_line,
                ModelFields.END_LINE: self.end_line,
                ModelFields.IS_DELETED: self.is_deleted
            }

        @staticmethod
        def from_json(file_ref):
            return DbDocumentModel.DbFileReferenceModel(
                file_ref[ModelFields.ID],
                file_ref[ModelFields.GITHUB_ACCOUNT_LOGIN],
                file_ref[ModelFields.REPO_NAME],
                file_ref[ModelFields.PATH],
                int(file_ref[ModelFields.START_LINE]),
                int(file_ref[ModelFields.END_LINE]),
                file_ref[ModelFields.IS_DELETED]
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
            ModelFields.GITHUB_ACCOUNT_LOGIN: self.github_account_login,
            ModelFields.NAME: self.name,
            ModelFields.CONTENT: self.content,
            ModelFields.REFS: [ref.to_json() for ref in self.refs] if self.refs is not None else None,
        }

    @staticmethod
    def from_json(document):
        return DbDocumentModel(
            document[ModelFields.GITHUB_ACCOUNT_LOGIN],
            document[ModelFields.NAME],
            document[ModelFields.CONTENT],
            [DbDocumentModel.DbFileReferenceModel.from_json(ref) for ref in document[ModelFields.REFS]]
        )
