from git_parser.git_patch_parser import GitPatchParser
from mongo.collection_clients.clients.db_doc_client import DbDocClient
from tools import logger
from webhook.handlers.actions.abstract_webhook_action import AbstractWebhookAction


class UpdateDocsRefsAction(AbstractWebhookAction):
    """
    Update the database references according to the commit files and how they affected those references.
    """

    def __init__(self, github_account_login, ref_commit_file_pairs):
        self.__github_account_login = github_account_login
        self.__ref_commit_file_pairs = ref_commit_file_pairs

    def perform(self):
        for ref_github_file_pairs in self.__ref_commit_file_pairs:
            self.__update_db_ref_state(
                self.__github_account_login,
                ref_github_file_pairs.ref,
                ref_github_file_pairs.commit_file
            )

    def __update_db_ref_state(self, github_account_login, ref, commit_file):
        logger.get_logger().info("Updating the documents references for github account login %s and references commit file pairs %s",
                                 str(self.__github_account_login), str(self.__ref_commit_file_pairs))

        diff_parser = GitPatchParser(commit_file)
        updated_line_range = diff_parser.calculate_updated_line_range(ref.start_line,
                                                                      ref.end_line)

        DbDocClient().update(
            ref.id,
            github_account_login,
            commit_file.path,
            updated_line_range["updated_start_line"],
            updated_line_range["updated_end_line"],
            commit_file.is_deleted
        )
