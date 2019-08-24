from git_parser.git_diff_parser import GitDiffParser
from mongo.collection_clients.clients.db_document_client import DbDocumentClient
from webhook.handlers.actions.abstract_webhook_action import AbstractWebhookAction


class UpdateDocsRefsAction(AbstractWebhookAction):

    def __init__(self, github_account_login, repo, ref_commit_file_pairs):
        self.__github_account_login = github_account_login
        self.__repo = repo
        self.__ref_commit_file_pairs = ref_commit_file_pairs

    def perform(self):
        for ref_github_file_pairs in self.__ref_commit_file_pairs:
            self.__update_db_ref_state(
                self.__github_account_login,
                ref_github_file_pairs.ref,
                ref_github_file_pairs.commit_file
            )

    def __update_db_ref_state(self, github_account_login, ref, commit_file):
        diff_parser = GitDiffParser(commit_file)
        updated_line_range = diff_parser.calculate_updated_line_range(ref.start_line,
                                                                      ref.end_line)

        DbDocumentClient().update(
            ref.id,
            github_account_login,
            commit_file.path,
            updated_line_range["updated_start_line"],
            updated_line_range["updated_end_line"],
            commit_file.is_deleted
        )
