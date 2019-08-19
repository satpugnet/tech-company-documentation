from mongo.constants.db_fields import DbFields
from utils.json.jsonable import Jsonable


class DbDocumentModel(Jsonable):
    """
    Represents a file of documentation, which will contain reference to code lines
    """

    class DbFileReferenceModel(Jsonable):
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
                DbFields.REF_ID_FIELD: self.ref_id,
                DbFields.GITHUB_ACCOUNT_LOGIN_FIELD: self.github_account_login,
                DbFields.REPO_NAME_FIELD: self.repo_name,
                DbFields.PATH_FIELD: self.path,
                DbFields.START_LINE_FIELD: self.start_line,
                DbFields.END_LINE_FIELD: self.end_line,
                DbFields.IS_DELETED_FIELD: self.is_deleted
            }

        @staticmethod
        def from_json(file_ref):
            return DbDocumentModel.DbFileReferenceModel(
                file_ref[DbFields.REF_ID_FIELD],
                file_ref[DbFields.GITHUB_ACCOUNT_LOGIN_FIELD],
                file_ref[DbFields.REPO_NAME_FIELD],
                file_ref[DbFields.PATH_FIELD],
                int(file_ref[DbFields.START_LINE_FIELD]),
                int(file_ref[DbFields.END_LINE_FIELD]),
                file_ref[DbFields.IS_DELETED_FIELD]
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
            DbFields.GITHUB_ACCOUNT_LOGIN_FIELD: self.github_account_login,
            DbFields.NAME_FIELD: self.name,
            DbFields.CONTENT_FIELD: self.content,
            DbFields.REFS_FIELD: [ref.to_json() for ref in self.refs] if self.refs is not None else None,
        }

    @staticmethod
    def from_json(document):
        return DbDocumentModel(
            document[DbFields.GITHUB_ACCOUNT_LOGIN_FIELD],
            document[DbFields.NAME_FIELD],
            document[DbFields.CONTENT_FIELD],
            [DbDocumentModel.DbFileReferenceModel.from_json(ref) for ref in document[DbFields.REFS_FIELD]]
        )
