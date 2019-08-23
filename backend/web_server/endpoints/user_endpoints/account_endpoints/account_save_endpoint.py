from flask import request
from flask_restful import abort

from mongo.collection_clients.clients.db_document_client import DbDocumentClient
from mongo.constants.db_fields import ModelFields
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountSaveEndpoint(AbstractAccountEndpoint):

    # TODO: Need to verify what data we get as an input (sanitize the data)
    def post(self, github_account_login):
        if DbDocumentClient().find_one(github_account_login, request.get_json()["name"]):
            return abort(400, message='Document name already exists')

        new_doc = request.get_json()
        new_doc[ModelFields.GITHUB_ACCOUNT_LOGIN] = github_account_login

        DbDocumentClient().insert_one(new_doc)

        return self._create_response({})
