from git_parser.git_diff_parser import GitDiffParser
from github_interface.interfaces.non_authenticated_github_interface import NonAuthenticatedGithubInterface
from mongo.collection_clients.clients.db_document_client import DbDocumentClient
from mongo.collection_clients.clients.db_github_file_client import DbGithubFileClient
from mongo.collection_clients.clients.db_repo_client import DbRepoClient
from mongo.models.db_doc_model import DbDocModel


class PushAndPRRequestHandler:
    def __init__(self, github_account_login, repo_name):
        self.__github_account_login = github_account_login
        self.__repo_interface = NonAuthenticatedGithubInterface(self.__github_account_login).request_repo(repo_name)

    def enact_push_event(self):
        commits = self.__get_commits_from_db_sha()

        for commit in commits:
            DbRepoClient().upsert_one_sha_last_update_only(self.__github_account_login, self.__repo_interface.repo.name, commit.sha)
            self.__update_db_files(commit.files)

    def enact_pull_request_opened_event(self, issue_number):
        pull_request_files = self.__repo_interface.get_pull_request_files(issue_number)

        self.__apply_pr_or_commit_updates(pull_request_files, True, issue_number,
                                          "This pull request has affected the following documentation files: \n")

    def __get_commits_from_db_sha(self):
        repo = DbRepoClient().find_one(self.__repo_interface.repo.name)
        sha_last_update = repo.sha_last_update if repo else None
        return self.__repo_interface.get_commits_since_sha_exclusive(sha_last_update, branch_name="master")

    def __update_db_files(self, commit_files):
        for commit_file_path in [commit_file.path for commit_file in commit_files]:
            up_to_date_file = self.__repo_interface.get_fs_node_at_path(commit_file_path)
            DbGithubFileClient().update_one(self.__github_account_login, self.__repo_interface.repo.name, up_to_date_file.dir_path,
                                        up_to_date_file.name, up_to_date_file.type, up_to_date_file.content)

    # TODO: split the 2 utilities of the method in different functions or classes
    # TODO: put the logic somewhere else
    def __apply_pr_or_commit_updates(self, commit_files, is_pull_request, issue_number_or_commit_sha, comment_message):
        name_commit_files = [commit_file.previous_path for commit_file in commit_files]
        affected_refs = []

        for document in DbDocumentClient().find(self.__github_account_login):
            document_json = document.to_json()
            has_refs_been_affected = False
            for ref in document_json[DbDocModel.REFS_FIELD]:
                if self.__is_ref_affected(ref, name_commit_files):
                    commit_file = list(filter(lambda x: x.previous_path == ref[DbDocModel.DbRefModel.PATH_FIELD], commit_files))[0]
                    has_refs_been_affected = True if \
                        GitDiffParser(commit_file).has_line_range_changed(ref[DbDocModel.DbRefModel.START_LINE_FIELD], ref[DbDocModel.DbRefModel.END_LINE_FIELD]) else has_refs_been_affected
                    if not is_pull_request:
                        self.__update_document_ref_state(commit_file, ref)
            if has_refs_been_affected:
                affected_refs.append("http://localhost:8080/" + str(document_json[DbDocModel.GITHUB_ACCOUNT_LOGIN_FIELD]) + "/docs/" +
                                     str(document_json[DbDocModel.NAME_FIELD]).replace(" ", "-"))

        if len(affected_refs) > 0:
            if is_pull_request:
                self.__repo_interface.post_pull_request_comment(issue_number_or_commit_sha, comment_message + '\n'.join(affected_refs))
            else:
                self.__repo_interface.post_commit_comment(issue_number_or_commit_sha, comment_message + '\n'.join(affected_refs))

    def __update_document_ref_state(self, commit_file, ref):
        diff_parser = GitDiffParser(commit_file)
        updated_line_range = diff_parser.calculate_updated_line_range(ref[DbDocModel.DbRefModel.START_LINE_FIELD], ref[DbDocModel.DbRefModel.END_LINE_FIELD])

        DbDocumentClient().update(
            ref[DbDocModel.DbRefModel.ID_FIELD],
            self.__github_account_login,
            updated_line_range["updated_start_line"],
            updated_line_range["updated_end_line"],
            commit_file.path,
            commit_file.is_deleted
        )

    def __is_ref_affected(self, ref, name_commit_files):
        return ref[DbDocModel.DbRefModel.GITHUB_ACCOUNT_LOGIN_FIELD] == self.__repo_interface.repo.github_account_login and \
               ref[DbDocModel.DbRefModel.REPO_NAME_FIELD] == self.__repo_interface.repo.name and ref[DbDocModel.DbRefModel.PATH_FIELD] in name_commit_files

