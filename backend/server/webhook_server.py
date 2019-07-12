import json

from flask import jsonify, request, abort, Blueprint

from github_interface.interface import GithubInterface
from mongo.models import Document
from utils.constants import GITHUB_WEBHOOK_SECRET

webhook_server = Blueprint('webhook_server', __name__,)


@webhook_server.route("/webhook_handler", methods=['POST'])
def webhook_handler():
    print("Webhook has been called")
    signature = request.headers['X-Hub-Signature']
    body = request.get_data()

    if not GithubInterface.verify_signature(signature, body, GITHUB_WEBHOOK_SECRET):
        abort(401)

    data = json.loads(request.data.decode("utf-8"))
    repo = GithubInterface.get_repo(data["repository"]["full_name"])

    for commit in data["commits"]:
        ref = data["ref"]
        if __is_branch_master(ref):
            sha = commit["id"]
            commit_files = repo.get_commit_files(sha=sha)
            __update_db_ref_line_numbers(repo.full_name, commit_files)

    response = jsonify({})

    return response

def __is_branch_master(ref):
    return ref[ref.rfind('/') + 1:] == "master"

def __update_db_ref_line_numbers(repo_name, commit_files):
    name_commit_files = [commit_file.previous_path for commit_file in commit_files]

    for document in Document.get_all():
        document_json = document.to_json()
        for ref in document_json["refs"]:

            if ref["repo"] == repo_name and ref["path"] in name_commit_files:
                commit_file = list(filter(lambda x: x.previous_path == ref["path"], commit_files))[0]
                updated_line_range = commit_file.calculate_updated_line_range(ref["start_line"], ref["end_line"])
                Document.update_lines_ref(ref["ref_id"], updated_line_range[0], updated_line_range[1])

                if commit_file.has_path_changed:
                    Document.update_path_ref(ref["ref_id"], commit_file.path)

                if commit_file.is_deleted:
                    Document.update_is_deleted_ref(ref["ref_id"], True)
