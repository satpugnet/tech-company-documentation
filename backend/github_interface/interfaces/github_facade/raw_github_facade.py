import requests
from github import Github, GithubIntegration

from github_interface.interfaces.github_facade.github_exception_handler import GithubExceptionHandler
from tools import logger


class RawGithubFacade:
    """
    A facade for communicating with github, used by the interfaces to access the github api.
    ALL CALLS TO THE GITHUB API SHOULD BE MADE USING THIS CLASS AND SUBCLASSES.
    """

    class UserFacade:
        """
        A facade for communicating with github with a user token
        """

        def __init__(self, user_token):
            # This one is for user to server request
            self.__user_token = user_token
            self.__user_github_object = Github(user_token)

        @GithubExceptionHandler.github_exception_handler
        def get_user(self):
            logger.get_logger().warning("Github, with user token, GET user")

            return self.__user_github_object.get_user()

        @GithubExceptionHandler.github_exception_handler
        def get_repo(self, repo_full_name):
            logger.get_logger().warning("Github, with user token, GET repo %s", repo_full_name)

            return self.__user_github_object.get_repo(repo_full_name)

        @GithubExceptionHandler.github_exception_handler
        def get_organization_repos(self, github_account_login):
            logger.get_logger().warning("Github, with user token, GET organization repos for %s", github_account_login)

            return self.__user_github_object.get_organization(github_account_login).get_repos()

        @GithubExceptionHandler.github_exception_handler
        def get_current_user_repos(self):
            logger.get_logger().warning("Github, with user token, GET current user repos")

            return self.__user_github_object.get_user().get_repos()

        @GithubExceptionHandler.github_exception_handler
        def get_repos(self, github_account_login):
            logger.get_logger().warning("Github, with user token, GET repos for %s", github_account_login)

            return self.__user_github_object.get_user(github_account_login).get_repos()

        @GithubExceptionHandler.github_exception_handler
        def get_user_installations(self):
            logger.get_logger().warning("Github, with user token, GET user installations")

            return requests.get(url="https://api.github.com/user/installations",
                                headers={
                                    "Authorization": "token " + self.__user_token,
                                    "Accept": "application/vnd.github.machine-man-preview+json"
                                })

    class InstallationFacade:
        """
        A facade for communicating with github with an installation token
        """

        def __init__(self, installation_token):
            # This one is for server to server requests
            self.__installation_github_object = Github(installation_token)

        @GithubExceptionHandler.github_exception_handler
        def get_repo(self, repo_full_name):
            logger.get_logger().warning("Github, with installation token, GET repos for %s", repo_full_name)

            return self.__installation_github_object.get_repo(repo_full_name)

        @GithubExceptionHandler.github_exception_handler
        def get_repos(self):
            logger.get_logger().warning("Github, with installation token, GET repos")

            return self.__installation_github_object.get_installation(-1).get_repos()

    class RepoFacade:
        """
        A facade for communicating with github, specifically for github repo information
        """

        def __init__(self, repo_object):
            self.__repo_object = repo_object

        @GithubExceptionHandler.github_exception_handler
        def get_contents(self, path):
            logger.get_logger().warning("Github repo, GET content at %s", path)

            return self.__repo_object.get_contents(path)

        @GithubExceptionHandler.github_exception_handler
        def get_commit(self, sha):
            logger.get_logger().warning("Github repo, GET commit for sha %s", sha)

            return self.__repo_object.get_commit(sha)

        @GithubExceptionHandler.github_exception_handler
        def get_commits(self, branch_name):
            logger.get_logger().warning("Github repo, GET commits for branch %s", branch_name)

            return self.__repo_object.get_commits(branch_name)

        @GithubExceptionHandler.github_exception_handler
        def get_branch_commit(self, branch_name):
            logger.get_logger().warning("Github repo, GET branch commit for branch %s", branch_name)

            return self.__repo_object.get_branch(branch_name).commit

        @GithubExceptionHandler.github_exception_handler
        def create_pull_issue_comment(self, issue_number, comment_text):
            logger.get_logger().warning("Github repo, CREATE pull issue comment for issue number %s", issue_number)

            self.__repo_object.get_pull(issue_number).create_issue_comment(comment_text)

        @GithubExceptionHandler.github_exception_handler
        def create_commit_comment(self, sha, comment_text):
            logger.get_logger().warning("Github repo, GET commit comment for sha %s", sha)

            self.__repo_object.get_commit(sha).create_comment(comment_text)

        @GithubExceptionHandler.github_exception_handler
        def get_pull_files(self, issue_number):
            logger.get_logger().warning("Github repo, GET pull files for issue number %s", issue_number)

            return self.__repo_object.get_pull(issue_number).get_files()

    @staticmethod
    @GithubExceptionHandler.github_exception_handler
    def get_access_token(github_app_identifier, private_key, installation_id):
        logger.get_logger().warning("Retrieving installation access token for installation id %s", installation_id)

        github_integration_object = GithubIntegration(github_app_identifier, private_key)

        return github_integration_object.get_access_token(installation_id)


