import json

from flask import jsonify, request, abort, Blueprint

from github_interface.interface import GithubInterface
from mongo.models.document import Document
from mongo.models.repository import Repository
from utils.constants import GITHUB_WEBHOOK_SECRET

webhook_server = Blueprint('webhook_server', __name__,)


@webhook_server.route("/webhook_handler", methods=['POST'])
def webhook_handler():
    print("Webhook has been called")
    if not __signature_valid():
        abort(401)

    __update_db()

    response = jsonify({})

    return response

def __update_db():
    data = json.loads(request.data.decode("utf-8"))
    repo = GithubInterface.get_repo(data["repository"]["full_name"])

    commits = __get_commits_from_db_sha(repo)

    # commits =__get_commits_from_webhook(data, repo)

    for commit in commits:
        Repository.upsert_sha_last_update(repo.full_name, commit.sha)
        __update_db_ref_line_numbers(repo.full_name, commit)

def __signature_valid():
    signature = request.headers['X-Hub-Signature']
    body = request.get_data()
    return GithubInterface.verify_signature(signature, body, GITHUB_WEBHOOK_SECRET)


def __get_commits_from_db_sha(repo):
    sha_last_update = Repository.find(repo.full_name).sha_last_update
    return repo.get_commits_since_sha_exclusive(sha_last_update)

def __get_commits_from_webhook(data, repo):
    commits = []
    for commit in data["commits"]:
        ref = data["ref"]
        if __is_branch_master(ref):
            sha = commit["id"]
            commits.append(repo.get_commit(sha=sha))
    return commits

def __is_branch_master(ref):
    return ref[ref.rfind('/') + 1:] == "master"

def __update_db_ref_line_numbers(repo_name, commit):
    name_commit_files = [commit_file.previous_path for commit_file in commit.files]

    for document in Document.get_all():
        document_json = document.to_json()
        for ref in document_json["refs"]:

            if ref["repo"] == repo_name and ref["path"] in name_commit_files:
                commit_file = list(filter(lambda x: x.previous_path == ref["path"], commit.files))[0]
                updated_line_range = commit_file.calculate_updated_line_range(ref["start_line"], ref["end_line"])
                Document.update_lines_ref(ref["ref_id"], updated_line_range[0], updated_line_range[1])

                if commit_file.has_path_changed:
                    Document.update_path_ref(ref["ref_id"], commit_file.path)

                if commit_file.is_deleted:
                    Document.update_is_deleted_ref(ref["ref_id"], True)
