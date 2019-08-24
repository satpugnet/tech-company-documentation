from github_interface.constants.github_api_fields import GithubApiFields
from github_interface.interfaces.webhook_github_interface import WebhookGithubInterface
from webhook.handlers.abstract_request_handler import AbstractRequestHandler
from webhook.handlers.actions.compute_affected_docs_action import ComputeAffectedDocsAction
from webhook.handlers.actions.post_comment_to_github_action import PostCommentToGithubAction


class PROpenedHandler(AbstractRequestHandler):

    def __init__(self, data):
        super().__init__()
        self.__issue_number = data[GithubApiFields.NUMBER]

        self.__github_account_login = data[GithubApiFields.REPOSITORY][GithubApiFields.OWNER][GithubApiFields.LOGIN]

        self.__repo_interface = WebhookGithubInterface(self.__github_account_login).request_repo(
            data[GithubApiFields.REPOSITORY][GithubApiFields.NAME]
        )

        self.__pr_files = self.__repo_interface.get_pull_request_files(self.__issue_number)

    def enact(self):
        affected_docs, _ = ComputeAffectedDocsAction(
            self.__github_account_login,
            self.__repo_interface.repo,
            self.__pr_files
        ).perform()

        PostCommentToGithubAction(
            self.__repo_interface,
            affected_docs,
            True,
            self.__issue_number
        ).perform()

