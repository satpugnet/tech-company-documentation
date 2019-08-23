from mongo.constants.model_fields import ModelFields
from mongo.models.abstract_db_collection_model import AbstractDbCollectionModel


# TODO: those could be simplify much further using marshmallow library or the **kwargs and a dictionary to create a generic function
from tools.json.jsonable import Jsonable


class DbDocModel(AbstractDbCollectionModel):
    """
    Represents a file of documentation, which will contain reference to code lines
    """

    class DbRefModel(Jsonable):
        """
        A FileReferenceModel is part of a Document, and references lines of code in repositories
        """

        ID_FIELD = ModelFields.ID
        GITHUB_ACCOUNT_LOGIN_FIELD = ModelFields.GITHUB_ACCOUNT_LOGIN
        REPO_NAME_FIELD = ModelFields.REPO_NAME
        PATH_FIELD = ModelFields.PATH
        START_LINE_FIELD = ModelFields.START_LINE
        END_LINE_FIELD = ModelFields.END_LINE
        IS_DELETED_FIELD = ModelFields.IS_DELETED

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
                DbDocModel.DbRefModel.ID_FIELD: self.id,
                DbDocModel.DbRefModel.GITHUB_ACCOUNT_LOGIN_FIELD: self.github_account_login,
                DbDocModel.DbRefModel.REPO_NAME_FIELD: self.repo_name,
                DbDocModel.DbRefModel.PATH_FIELD: self.path,
                DbDocModel.DbRefModel.START_LINE_FIELD: self.start_line,
                DbDocModel.DbRefModel.END_LINE_FIELD: self.end_line,
                DbDocModel.DbRefModel.IS_DELETED_FIELD: self.is_deleted
            }

        @staticmethod
        def from_json(file_ref):
            return DbDocModel.DbRefModel(
                file_ref[DbDocModel.DbRefModel.ID_FIELD],
                file_ref[DbDocModel.DbRefModel.GITHUB_ACCOUNT_LOGIN_FIELD],
                file_ref[DbDocModel.DbRefModel.REPO_NAME_FIELD],
                file_ref[DbDocModel.DbRefModel.PATH_FIELD],
                int(file_ref[DbDocModel.DbRefModel.START_LINE_FIELD]),
                int(file_ref[DbDocModel.DbRefModel.END_LINE_FIELD]),
                file_ref[DbDocModel.DbRefModel.IS_DELETED_FIELD]
            )

    GITHUB_ACCOUNT_LOGIN_FIELD = ModelFields.GITHUB_ACCOUNT_LOGIN
    NAME_FIELD = ModelFields.NAME
    CONTENT_FIELD = ModelFields.CONTENT
    REFS_FIELD = ModelFields.REFS

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
            DbDocModel.GITHUB_ACCOUNT_LOGIN_FIELD: self.github_account_login,
            DbDocModel.NAME_FIELD: self.name,
            DbDocModel.CONTENT_FIELD: self.content,
            DbDocModel.REFS_FIELD: [ref.to_json() for ref in self.refs] if self.refs is not None else None,
        }

    @staticmethod
    def from_json(document):
        return DbDocModel(
            document[DbDocModel.GITHUB_ACCOUNT_LOGIN_FIELD],
            document[DbDocModel.NAME_FIELD],
            document[DbDocModel.CONTENT_FIELD],
            [DbDocModel.DbRefModel.from_json(ref) for ref in document[DbDocModel.REFS_FIELD]]
        )
