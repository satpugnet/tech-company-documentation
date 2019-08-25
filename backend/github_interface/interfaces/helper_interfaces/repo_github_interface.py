from github_interface.wrappers.factories.github_fs_node_factory import GithubFSNodeFactory
from github_interface.wrappers.models.git_commit_model import GithubCommitModel
from github_interface.wrappers.models.github_commit_file_model import GithubCommitFileModel
from github_interface.wrappers.models.github_repo_model import GithubRepoModel
from tools import logger


class RepoGithubInterface:
    """
    An interface to access a github repo and its informations.
    """

    def __init__(self, raw_repo):
        self.__repo_object = raw_repo
        self.__repo = GithubRepoModel(raw_repo.owner.login, raw_repo.name, raw_repo.full_name, raw_repo.owner.type, bool(raw_repo.private))

    @property
    def repo(self):
        return self.__repo

    def get_all_files_flat(self):
        """
        :return: Returns all the files For github repository as a list of GithubFileModel.
        """
        logger.get_logger().warning("For github repository %s, getting to github all the files", self.__repo.full_name)

        files = []

        contents = self.__repo_object.get_contents("")
        while contents:
            content = contents.pop(0)
            if content.type == "dir":
                contents.extend(self.__repo_object.get_contents(content.path))
            else:
                files.append(GithubFSNodeFactory().create_from_github_get_contents(content))

        return files

    def get_fs_node_at_path(self, path=""):
        """
        :return: Returns the file system node present at the given path.
        """
        logger.get_logger().warning("For github repository %s, requesting to github all the file system node at path %s", self.__repo.full_name, path)

        contents = self.__repo_object.get_contents(path)
        return GithubFSNodeFactory().create_from_github_get_contents(contents)

    def get_commits_since_sha_exclusive(self, sha, branch_name="master"):
        """
        :return: Returns all commits pushed on the given branch since the given sha.
        """
        logger.get_logger().warning("For github repository %s, getting all commits since sha %s and branch %s", self.__repo.full_name, sha, branch_name)

        raw_commits = self.__repo_object.get_commits(branch_name)

        commits = []
        for commit in raw_commits:
            if commit.sha == sha:
                break
            commits.append(self.get_commit(sha=commit.sha))

        commits.reverse()

        return commits

    def get_commit(self, branch_name="master", sha=None):
        """
        :param branch_name: The branch to look at.
        :param sha: The specific sha to search.
        :return: A single GithubCommitModel.
        """
        logger.get_logger().warning("For github repository %s, getting the commit at branch %s (and with sha %s)", self.__repo.full_name, branch_name, sha)
        
        if sha:
            raw_commit = self.__repo_object.get_commit(sha)
        else:
            raw_commit = self.__repo_object.get_branch(branch_name).commit

        commit_files = []
        for file in raw_commit.files:
            commit_files.append(GithubCommitFileModel(file.filename, file.previous_filename, file.patch, file.status == "removed"))

        return GithubCommitModel(commit_files, raw_commit.sha)

    def post_pull_request_comment(self, issue_number, comment_text):
        """
        Post the comment on the pull request associated without the issue number.
        """
        logger.get_logger().warning("For github repository %s, posting a comment to pull request number %s", str(issue_number), self.__repo.full_name)

        self.__repo_object.get_pull(issue_number).create_issue_comment(comment_text)

    def post_commit_comment(self, sha, comment_text):
        """
        Post the comment on the commit associated without the sha.
        """
        logger.get_logger().warning("For github repository %s, posting a comment to push commit with sha %s", self.__repo.full_name, sha)

        self.__repo_object.get_commit(sha).create_comment(comment_text)

    def get_pull_request_files(self, issue_number):
        """
        TODO: The response of /repos/:owner/:repo/pulls/:pull_number/files is a maximum of 300 files, a way around this needs to be implemented
        :param issue_number: The issue number associated with the pull_request (issue number and pull request number are the same in Github).
        :return: A list of GithubCommitFile.
        """
        logger.get_logger().warning("For github repository %s, getting the pull request files for pull request number %s", self.__repo.full_name, str(issue_number))

        pr_files = self.__repo_object.get_pull(issue_number).get_files()
        return [GithubCommitFileModel(file.filename, None, file.patch, file.status == "removed") for file in pr_files]
