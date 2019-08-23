from mongo.collection_clients.clients.db_document_client import DbDocumentClient
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountDocsEndpoint(AbstractAccountEndpoint):

    def get(self, github_account_login):

        docs = DbDocumentClient().find(github_account_login)

        return self._create_response([doc for doc in docs])
