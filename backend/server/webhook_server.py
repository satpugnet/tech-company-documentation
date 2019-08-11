import json

from flask import jsonify, request, abort, Blueprint

from github_interface.authorisation_interface import GithubAuthorisationInterface
from utils.constants import GITHUB_WEBHOOK_SECRET
from webhook.webhook_request_handler import WebhookRequestHandler

webhook_server = Blueprint('webhook_server', __name__)

@webhook_server.route("/webhook_handler", methods=['POST'])
def webhook_handler():
    print("Webhook has been called for " + str(request.headers['x-github-event']))
    if not __signature_valid():
        abort(401)

    event_type = request.headers['x-github-event']
    data = json.loads(request.data.decode("utf-8"))
    request_handler = WebhookRequestHandler(data["repository"]["owner"]["login"], data["repository"]["full_name"])

    if event_type == "push":
        if __is_branch_master(data["ref"]):
            request_handler.enact_push_event()
    elif event_type == "pull_request" and data["action"] == "opened":
        request_handler.enact_pull_request_event(data["number"])

    response = jsonify({})
    return response

def manually_update_db(organisation_login, repo_full_name):
    WebhookRequestHandler(organisation_login, repo_full_name).enact_push_event()

def __signature_valid():
    signature = request.headers['X-Hub-Signature']
    body = request.get_data()
    return GithubAuthorisationInterface.verify_signature(signature, body, GITHUB_WEBHOOK_SECRET)

def __is_branch_master(ref):
    return ref[ref.rfind('/') + 1:] == "master"
