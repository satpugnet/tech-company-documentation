from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.models.db_document_model import DbDocumentModel


class DbDocumentClient(AbstractDbCollectionClient):
    """
    Represents a document
    """

    def __init__(self):
        super().__init__('document', DbDocumentModel)

    def update_one_lines_ref(self, github_account_login, ref_id, start_line, end_line):
        return self._update_one(DbDocumentModel(github_account_login=github_account_login, refs=[DbDocumentModel.FileReferenceModel(ref_id=ref_id)]),
                                DbDocumentModel(refs=DbDocumentModel.FileReferenceModel(start_line=start_line, end_line=end_line)))

    def update_one_path_ref(self, github_account_login, ref_id, path):
        return self._update_one(DbDocumentModel(github_account_login=github_account_login, refs=[DbDocumentModel.FileReferenceModel(ref_id=ref_id)]),
                                DbDocumentModel(refs=DbDocumentModel.FileReferenceModel(path=path)))

    def update_one_is_deleted_ref(self, github_account_login, ref_id, is_deleted):
        return self._update_one(DbDocumentModel(github_account_login=github_account_login, refs=[DbDocumentModel.FileReferenceModel(ref_id=ref_id)]),
                                DbDocumentModel(refs=DbDocumentModel.FileReferenceModel(is_deleted=is_deleted)))

    def find_one(self, github_account_login, name):
        return self._find_one(DbDocumentModel(github_account_login=github_account_login, name=name))

    def find(self, github_account_login):
        return self._find(DbDocumentModel(github_account_login=github_account_login))

