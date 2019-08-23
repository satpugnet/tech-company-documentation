from flask import session, request
from flask_restful import abort

from github_interface.interfaces.github_authorisation_interface import GithubAuthorisationInterface
from mongo.collection_clients.clients.db_user_client import DbUserClient
from utils.secret_constant import SecretConstant
from web_server.endpoints.abstract_endpoint import AbstractEndpoint


class AuthGithubCallbackEndpoint(AbstractEndpoint):

    def post(self):
        temporary_code = request.args['code']
        state = request.args['state']

        if state != SecretConstant.SECRET_PASSWORD_FORGERY:
            abort(401, message="Unauthenticated request")

        user_token = GithubAuthorisationInterface.request_user_token(SecretConstant.CLIENT_ID, SecretConstant.CLIENT_SECRET,
                                                                     temporary_code, SecretConstant.REDIRECT_URL_LOGIN)

        session[AbstractEndpoint.USER_LOGIN_FIELD] = GithubAuthorisationInterface.request_user_login(user_token)

        # TODO: remove the upsert one line once the upsert one is changed into an insert and done in the webhook
        DbUserClient().upsert_one_user_token(session[AbstractEndpoint.USER_LOGIN_FIELD], user_token)

        return self._create_response({})
