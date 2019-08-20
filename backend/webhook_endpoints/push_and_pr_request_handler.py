from git_parser.git_diff_parser import GitDiffParser
from github_interface.interfaces.non_authenticated_github_interface import NonAuthenticatedGithubInterface
from mongo.collection_clients.db_document_client import DbDocumentClient
from mongo.collection_clients.db_repo_client import DbRepoClient
from mongo.collection_clients.db_github_file_client import DbGithubFileClient
from mongo.constants.db_fields import ModelFields


class PushAndPRRequestHandler:
    def __init__(self, github_account_login, repo_name):
        self.__github_account_login = github_account_login
        self.__repo_interface = NonAuthenticatedGithubInterface(self.__github_account_login).request_repo(repo_name)

    def enact_push_event(self):
        commits = self.__get_commits_from_db_sha()

        for commit in commits:
            DbRepoClient().upsert_sha_last_update_only(self.__github_account_login, self.__repo_interface.repo.name, commit.sha)
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
            DbGithubFileClient().upsert(self.__github_account_login, self.__repo_interface.repo.name, up_to_date_file.dir_path,
                                        up_to_date_file.name, up_to_date_file.type, up_to_date_file.content)

    # TODO: split the 2 utilities of the method in different functions or classes
    def __apply_pr_or_commit_updates(self, commit_files, is_pull_request, issue_number_or_commit_sha, comment_message):
        name_commit_files = [commit_file.previous_path for commit_file in commit_files]
        affected_refs = []

        for document in DbDocumentClient().find(self.__github_account_login):
            document_json = document.to_json()
            has_refs_been_affected = False
            for ref in document_json[ModelFields.REFS]:
                if self.__is_ref_affected(ref, name_commit_files):
                    commit_file = list(filter(lambda x: x.previous_path == ref[ModelFields.PATH], commit_files))[0]
                    has_refs_been_affected = True if \
                        GitDiffParser(commit_file).has_line_range_changed(ref[ModelFields.START_LINE], ref[ModelFields.END_LINE]) else has_refs_been_affected
                    if not is_pull_request:
                        self.__update_document_ref_state(commit_file, ref)
            if has_refs_been_affected:
                affected_refs.append("http://localhost:8080/" + str(document_json[ModelFields.GITHUB_ACCOUNT_LOGIN]) + "/docs/" +
                                     str(document_json[ModelFields.NAME]).replace(" ", "-"))

        if len(affected_refs) > 0:
            if is_pull_request:
                self.__repo_interface.post_pull_request_comment(issue_number_or_commit_sha, comment_message + '\n'.join(affected_refs))
            else:
                self.__repo_interface.post_commit_comment(issue_number_or_commit_sha, comment_message + '\n'.join(affected_refs))

    def __update_document_ref_state(self, commit_file, ref):
        updated_line_range = GitDiffParser(commit_file).calculate_updated_line_range(ref[ModelFields.START_LINE], ref[ModelFields.END_LINE])
        DbDocumentClient().update_one_lines_ref(self.__github_account_login, ref[ModelFields.ID], updated_line_range[0], updated_line_range[1])
        if commit_file.has_path_changed:
            DbDocumentClient().update_one_path_ref(self.__github_account_login, ref[ModelFields.ID], commit_file.path)
        if commit_file.is_deleted:
            DbDocumentClient().update_one_is_deleted_ref(self.__github_account_login, ref[ModelFields.ID], True)

    def __is_ref_affected(self, ref, name_commit_files):
        return ref[ModelFields.GITHUB_ACCOUNT_LOGIN] == self.__repo_interface.repo.github_account_login and \
               ref[ModelFields.REPO_NAME] == self.__repo_interface.repo.name and ref[ModelFields.PATH] in name_commit_files

