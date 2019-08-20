from mongo.collection_clients.abstract_db_collection_client import AbstractDbCollectionClient
from mongo.constants.db_new_values_actions import DbNewValuesActions
from mongo.models.db_document_model import DbDocumentModel


class DbDocumentClient(AbstractDbCollectionClient):
    """
    Represents a document
    """

    def __init__(self):
        super().__init__('document', DbDocumentModel)

    def update_one_lines_ref(self, github_account_login, id, start_line, end_line):
        return self._update_one(
            DbDocumentModel(
                github_account_login=github_account_login,
                refs=[
                    DbDocumentModel.DbFileReferenceModel(
                        id=id
                    )
                ]
            ),
            DbDocumentModel(
                refs=DbDocumentModel.DbFileReferenceModel(
                    start_line=start_line,
                    end_line=end_line
                )
            ),
            DbNewValuesActions.SET_ACTION
        )

    def update_one_path_ref(self, github_account_login, id, path):
        return self._update_one(
            DbDocumentModel(
                github_account_login=github_account_login,
                refs=[
                    DbDocumentModel.DbFileReferenceModel(
                        id=id
                    )
                ]
            ),
            DbDocumentModel(
                refs=DbDocumentModel.DbFileReferenceModel(
                    path=path
                )
            ),
            DbNewValuesActions.SET_ACTION
        )

    def update_one_is_deleted_ref(self, github_account_login, id, is_deleted):
        return self._update_one(
            DbDocumentModel(
                github_account_login=github_account_login,
                refs=[
                    DbDocumentModel.DbFileReferenceModel(
                        id=id
                    )
                ]
            ),
            DbDocumentModel(
                refs=DbDocumentModel.DbFileReferenceModel(
                    is_deleted=is_deleted
                )
            ),
            DbNewValuesActions.SET_ACTION
        )

    def find_one(self, github_account_login, name):
        return self._find_one(
            DbDocumentModel(
                github_account_login=github_account_login,
                name=name
            )
        )

    def find(self, github_account_login):
        return self._find(
            DbDocumentModel(
                github_account_login=github_account_login
            )
        )

