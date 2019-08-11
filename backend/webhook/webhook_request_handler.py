from github_interface.non_authenticated_github_interface import NonAuthenticatedGithubInterface
from mongo.models.document import Document
from mongo.models.repository import Repository


class WebhookRequestHandler:

    def __init__(self, organisation_login, repo_full_name):
        self.__organisation_login = organisation_login
        self.__repo = NonAuthenticatedGithubInterface.get_repo(self.__organisation_login, repo_full_name)

    def enact_push_event(self):
        commits = self.__get_commits_from_db_sha()

        for commit in commits:
            Repository.upsert_sha_last_update(self.__repo.full_name, commit.sha)
            self.__apply_pr_or_commit_updates(commit.files, False, commit.sha, "This commit has affected the following documentation files: \n")

    def enact_pull_request_event(self, issue_number):
        repo = NonAuthenticatedGithubInterface.get_repo(self.__organisation_login, self.__repo.full_name)
        pull_request_files = repo.get_pull_request_files(issue_number)

        self.__apply_pr_or_commit_updates(pull_request_files, True, issue_number, "This pull request has affected the following documentation files: \n")

    def __get_commits_from_db_sha(self):
        sha_last_update = Repository.find(self.__repo.full_name).sha_last_update if Repository.find(self.__repo.full_name) else None
        return self.__repo.get_commits_since_sha_exclusive(sha_last_update, branch_name="master")

    def __apply_pr_or_commit_updates(self, commit_files, is_pull_request, issue_number_or_commit_sha, comment_message):
        name_commit_files = [commit_file.previous_path for commit_file in commit_files]
        affected_refs = []

        for document in Document.get_all(self.__organisation_login):
            document_json = document.to_json()
            has_refs_been_affected = False
            for ref in document_json["refs"]:
                if ref["repo"] == self.__repo.full_name and ref["path"] in name_commit_files:
                    commit_file = list(filter(lambda x: x.previous_path == ref["path"], commit_files))[0]
                    if commit_file.has_line_range_changed(ref["start_line"], ref["end_line"]):
                        has_refs_been_affected = True
                    if not is_pull_request:
                        self.__update_db_ref_state(commit_file, ref)
            if has_refs_been_affected:
                affected_refs.append("http://http://localhost:8080/" + str(document_json["organisation"]) + "/docs/" + str(document_json["name"]).replace(" ", "_"))

        if len(affected_refs) > 0:
            if is_pull_request:
                self.__repo.post_pull_request_comment(issue_number_or_commit_sha, comment_message + '\n'.join(affected_refs))
            else:
                self.__repo.post_commit_comment(issue_number_or_commit_sha, comment_message + '\n'.join(affected_refs))

    def __update_db_ref_state(self, commit_file, ref):
        updated_line_range = commit_file.calculate_updated_line_range(ref["start_line"], ref["end_line"])
        Document.update_lines_ref(self.__organisation_login, ref["ref_id"], updated_line_range[0], updated_line_range[1])
        if commit_file.has_path_changed:
            Document.update_path_ref(self.__organisation_login, ref["ref_id"], commit_file.path)
        if commit_file.is_deleted:
            Document.update_is_deleted_ref(self.__organisation_login, ref["ref_id"], True)
