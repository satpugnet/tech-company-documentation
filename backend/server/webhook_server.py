import json

from flask import jsonify, request, abort, Blueprint

from github_interface.security.signature_validator import SignatureValidator
from utils.global_constant import GlobalConst
from webhook_endpoints.installation_request_handler import InstallationRequestHandler
from webhook_endpoints.push_and_pr_request_handler import PushAndPRRequestHandler

webhook_server = Blueprint('webhook_server', __name__)


@webhook_server.route("/webhook_handler", methods=['POST'])
def webhook_handler():
    data = json.loads(request.data.decode("utf-8"))
    print("Webhook has been called for " + str(request.headers['x-github-event']) + " with action " +
          str(data["action"]) if "action" in data else "" )
    if not __signature_valid():
        abort(401)

    event_type = request.headers['x-github-event']

    if event_type == "push":
        request_handler = PushAndPRRequestHandler(data["repository"]["owner"]["login"], data["repository"]["name"])
        if __is_branch_master(data["ref"]):
            request_handler.enact_push_event()
    elif event_type == "pull_request" and data["action"] == "opened":
        request_handler = PushAndPRRequestHandler(data["repository"]["owner"]["login"], data["repository"]["name"])
        request_handler.enact_pull_request_opened_event(data["number"])
    elif event_type == "installation" and data["action"] == "created":
        request_handler = InstallationRequestHandler(data["installation"]["account"]["login"])
        request_handler.enact_installation_created_event([data_repo["name"] for data_repo in data["repositories"]], data["installation"]["id"])
    elif event_type == "installation" and data["action"] == "deleted":
        request_handler = InstallationRequestHandler(data["installation"]["account"]["login"])
        request_handler.enact_installation_deleted_event()

    response = jsonify({})
    return response

def manually_update_db(github_account_login, repo_name):
    PushAndPRRequestHandler(github_account_login, repo_name).enact_push_event()

def __signature_valid():
    signature = request.headers['X-Hub-Signature']
    body = request.get_data()
    return SignatureValidator().verify_signature(signature, body, GlobalConst.GITHUB_WEBHOOK_SECRET)


def __is_branch_master(ref):
    return ref[ref.rfind('/') + 1:] == "master"
