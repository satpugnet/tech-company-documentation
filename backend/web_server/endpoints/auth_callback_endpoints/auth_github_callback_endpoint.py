from flask import session, request
from flask_restful import abort

from github_interface.interfaces.github_authorisation_interface import GithubAuthorisationInterface
from mongo.collection_clients.clients.db_user_client import DbUserClient
from tools import logger
from utils.secret_constant import SecretConstant
from web_server.endpoints.abstract_endpoint import AbstractEndpoint


class AuthGithubCallbackEndpoint(AbstractEndpoint):
    """
    Endpoint for handling the auth github callback.
    """

    CODE_FIELD = "code"
    STATE_FIELD = "state"

    def post(self):
        temporary_code = request.args[self.CODE_FIELD]
        state = request.args[self.STATE_FIELD]

        if state != SecretConstant.SECRET_PASSWORD_FORGERY:
            logger.get_logger().error("The secret password for forgery is not valid.")
            abort(401, message="Unauthenticated request")

        user_token = GithubAuthorisationInterface.request_user_token(SecretConstant.CLIENT_ID, SecretConstant.CLIENT_SECRET,
                                                                     temporary_code, SecretConstant.REDIRECT_URL_LOGIN)

        session[AbstractEndpoint.COOKIE_USER_LOGIN_FIELD] = GithubAuthorisationInterface.request_user_login(user_token)

        # TODO: remove the upsert one line once the upsert one is changed into an insert and performed in the webhook
        DbUserClient().upsert_one_user_token(session[AbstractEndpoint.COOKIE_USER_LOGIN_FIELD], user_token)

        return self._create_empty_response()
