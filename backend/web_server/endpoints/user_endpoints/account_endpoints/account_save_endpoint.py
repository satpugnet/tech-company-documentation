from flask import request
from flask_restful import abort

from mongo.collection_clients.clients.db_doc_client import DbDocClient
from mongo.constants.model_fields import ModelFields
from mongo.models.db_doc_model import DbDocModel
from tools import logger
from web_server.endpoints.user_endpoints.account_endpoints.abstract_user_account_endpoint import AbstractAccountEndpoint


class AccountSaveEndpoint(AbstractAccountEndpoint):
    """
    Endpoint for handling the saving of docs.
    """

    def post(self, github_account_login):
        if DbDocClient().find_one(github_account_login, request.get_json()[ModelFields.NAME]):
            logger.get_logger().error("The document name %s already exist", request.get_json()[ModelFields.NAME])
            return abort(400, message='Document name already exists')

        new_doc = request.get_json()
        new_doc[DbDocModel.GITHUB_ACCOUNT_LOGIN_FIELD] = github_account_login

        DbDocClient().insert_one(new_doc)

        return self._create_empty_response()
