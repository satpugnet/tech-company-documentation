from github_interface.constants.github_api_fields import GithubApiFields
from github_interface.interfaces.webhook_github_interface import WebhookGithubInterface
from mongo.collection_clients.clients.db_github_file_client import DbGithubFileClient
from mongo.collection_clients.clients.db_repo_client import DbRepoClient
from utils.path_manipulator import PathManipulator
from webhook.handlers.abstract_request_handler import AbstractRequestHandler
from webhook.handlers.actions.compute_affected_docs_action import ComputeAffectedDocsAction
from webhook.handlers.actions.post_comment_to_github_action import PostCommentToGithubAction
from webhook.handlers.actions.update_docs_refs_action import UpdateDocsRefsAction


class PushHandler(AbstractRequestHandler):
    """
    A handler for push event.
    """

    def __init__(self, data):
        super().__init__()
        self.__branch = PathManipulator().dissociate_dir_path_from_fs_node_name(data[GithubApiFields.REF]).fs_node_name
        self.__github_account_login = data[GithubApiFields.REPOSITORY][GithubApiFields.OWNER][GithubApiFields.LOGIN]
        self.__repo_interface = WebhookGithubInterface(self.__github_account_login).request_repo(
            data[GithubApiFields.REPOSITORY][GithubApiFields.NAME]
        )

    def enact(self):
        if self.__branch != "master":
            return

        # TODO: create a complete handler for all missed commits
        # TODO: action must be more agnostic of all variables and only contain the required ones
        for commit in self.__retrieve_all_missed_commits():

            self.__update_db_github_files(commit.files)

            affected_docs, ref_commit_file_pairs = ComputeAffectedDocsAction(
                self.__github_account_login,
                self.__repo_interface.repo,
                commit.files
            ).perform()

            UpdateDocsRefsAction(
                self.__github_account_login,
                self.__repo_interface.repo,
                ref_commit_file_pairs
            ).perform()

            PostCommentToGithubAction(
                self.__repo_interface,
                affected_docs,
                False,
                commit.sha
            ).perform()

            self.__upsert_one_sha_last_update(commit.sha)

    def __upsert_one_sha_last_update(self, commit_sha):
        """
        Upsert the sha for teh last received commit in the database.
        """

        DbRepoClient().upsert_one_sha_last_update(
            self.__github_account_login,
            self.__repo_interface.repo.name,
            commit_sha
        )

    def __update_db_github_files(self, commit_files):
        """
        Update all of the affected mirrored github files in the database.
        """

        for commit_file_path in [commit_file.path for commit_file in commit_files]:
            up_to_date_file = self.__repo_interface.get_fs_node_at_path(commit_file_path)

            DbGithubFileClient().update_one(
                self.__github_account_login,
                self.__repo_interface.repo.name,
                up_to_date_file.dir_path,
                up_to_date_file.name,
                up_to_date_file.type,
                up_to_date_file.content
            )

    def __retrieve_all_missed_commits(self):
        """
        :return: Returns all of the commits since the last received commmit.
        """

        db_repo = DbRepoClient().find_one(
            self.__repo_interface.repo.name
        )

        return self.__repo_interface.get_commits_since_sha_exclusive(
            db_repo.sha_last_update,
            branch_name="master"
        )
