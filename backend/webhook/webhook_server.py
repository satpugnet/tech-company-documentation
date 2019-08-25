import json

from flask import jsonify, request, Blueprint
from flask_restful import abort

from github_interface.constants.github_api_fields import GithubApiFields
from github_interface.constants.github_api_values import GithubApiValues
from github_interface.constants.github_event_values import GithubEventValues
from github_interface.security.signature_validator import SignatureValidator
from tools import logger
from utils.secret_constant import SecretConstant
from webhook.handlers.installation_created_handler import InstallationCreatedHandler
from webhook.handlers.installation_deleted_handler import InstallationDeletedHandler
from webhook.handlers.pr_opened_handler import PROpenedHandler
from webhook.handlers.push_handler import PushHandler

webhook_server = Blueprint('webhook_server', __name__)


@webhook_server.route("/webhook_handler", methods=['POST'])
def webhook_handler():
    """
    Handle all the incoming github webhook request and delegate to the right handler.
    """

    data = json.loads(request.data.decode("utf-8"))
    logger.get_logger().warning("Webhook has been called for %s with action %s", request.headers['x-github-event'],
                             data[GithubApiFields.ACTION] if GithubApiFields.ACTION in data else "")

    if not __signature_valid():
        abort(401, message="Invalid signature")

    event_type = request.headers['x-github-event']

    if event_type == GithubEventValues.PUSH:
        PushHandler(data).enact()

    elif event_type == GithubEventValues.PULL_REQUEST and data[GithubApiFields.ACTION] == GithubApiValues.OPENED:
        PROpenedHandler(data).enact()

    elif event_type == GithubEventValues.INSTALLATION and data[GithubApiFields.ACTION] == GithubApiValues.CREATED:
        InstallationCreatedHandler(data).enact()

    elif event_type == GithubEventValues.INSTALLATION and data[GithubApiFields.ACTION] == GithubApiValues.DELETED:
        InstallationDeletedHandler(data).enact()

    return jsonify({})


def manually_update_db(github_account_login, repo_name):
    """
    Used to manually update the database without sending a push event. Used for development.
    """

    data = {}
    data[GithubApiFields.REPOSITORY][GithubApiFields.OWNER][GithubApiFields.LOGIN] = github_account_login
    data[GithubApiFields.REPOSITORY][GithubApiFields.NAME] = repo_name

    PushHandler(data).enact()


def __signature_valid():
    signature = request.headers['X-Hub-Signature']
    body = request.get_data()

    return SignatureValidator().verify_signature(signature, body, SecretConstant.GITHUB_WEBHOOK_SECRET)


