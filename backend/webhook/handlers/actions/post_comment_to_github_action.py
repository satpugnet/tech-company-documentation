from webhook.handlers.actions.abstract_webhook_action import AbstractWebhookAction


class PostCommentToGithubAction(AbstractWebhookAction):
    """
    Post a comment as a Github App in a github pull request or a github push.
    """

    PUSH_COMMENT_MESSAGE = "This commit has affected the following documentation files:"
    PR_COMMENT_MESSAGE = "This pull request has affected the following documentation files:"

    PUSH_NO_FILE_AFFECTED_COMMENT = "No documentation file were affected by this push."
    PR_NO_FILE_AFFECTED_COMMENT = "No documentation file were affected by this pull request."

    def __init__(self, repo_interface, affected_docs, is_pull_request, issue_number_or_commit_sha):
        self.__repo_interface = repo_interface
        self.__affected_docs = affected_docs
        self.__is_pull_request = is_pull_request
        self.__issue_number_or_commit_sha = issue_number_or_commit_sha

    def perform(self):
        message_lines = []
        for doc in self.__affected_docs:
            current_line = "http://localhost:8080/" + str(doc.github_account_login) + "/docs/" + str(doc.name)
            message_lines.append(current_line.replace(" ", "-"))

        if self.__is_pull_request:
            if len(message_lines) > 0:
                comment = PostCommentToGithubAction.PR_COMMENT_MESSAGE + '\n' + '\n'.join(message_lines)
            else:
                comment = PostCommentToGithubAction.PUSH_NO_FILE_AFFECTED_COMMENT

            self.__repo_interface.post_pull_request_comment(
                self.__issue_number_or_commit_sha,
                comment
            )
        else:
            if len(message_lines) > 0:
                comment = PostCommentToGithubAction.PUSH_COMMENT_MESSAGE + '\n' + '\n'.join(message_lines)

            else:
                comment = PostCommentToGithubAction.PR_NO_FILE_AFFECTED_COMMENT

            self.__repo_interface.post_commit_comment(
                self.__issue_number_or_commit_sha,
                comment
            )
