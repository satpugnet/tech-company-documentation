from flask import request

from mongo.collection_clients.clients.db_doc_client import DbDocClient
from mongo.models.db_doc_model import DbDocModel
from search import markdown_indexer
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountSaveEndpoint(AbstractAccountEndpoint):
    """
    Endpoint for handling the saving of docs.
    """

    def post(self, github_account_login):
        # FIXME: today, we can override docs if they have the same name, in the future, we will have a document id

        raise Exception("Problem")

        new_doc = request.get_json()
        new_doc[DbDocModel.GITHUB_ACCOUNT_LOGIN_FIELD] = github_account_login

        DbDocClient().insert_one(new_doc)

        # We index the new markdown document for search
        title = new_doc[DbDocModel.NAME_FIELD]
        content = new_doc[DbDocModel.CONTENT_FIELD]
        indexing_success = markdown_indexer.insert_markdown_doc(
            source='app',
            title=title,
            content=content
        )

        if not indexing_success:
            return self._create_error_response(code=400)

        return self._create_empty_response()
