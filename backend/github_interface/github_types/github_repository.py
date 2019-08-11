from github import UnknownObjectException

from github_interface.github_types.abstract_github_file import AbstractGithubFile
from github_interface.github_types.git_commit import GithubCommit
from github_interface.github_types.github_commit_file import GithubCommitFile
from github_interface.github_types.github_directory import GithubDirectory


class GithubRepository:
    def __init__(self, repo_object):
        self.__repo_object = repo_object
        self._full_name = self.__repo_object.full_name
        self._root_directory = self.__load_github_repo()
        self._owner = self.__initialiase_owner()
        self._private = bool(self.__repo_object.private)

    @property
    def full_name(self):
        return self._full_name

    @property
    def root_directory(self):
        return self._root_directory

    @property
    def owner(self):
        return self._owner

    @property
    def private(self):
        return self._private

    def get_content_at_path(self, path=""):
        path_files = self.__file_path_to_list(path)

        current_directory = self.root_directory

        for filename in path_files:
            current_directory = current_directory.load_subfiles()[filename]

        if current_directory.type == AbstractGithubFile.DIRECTORY:
            current_directory.load_subfiles()

        return current_directory

    def get_lines_at_path(self, path, start_line, end_line):
        return self.get_content_at_path(path).content.splitlines()[start_line - 1: end_line]

    def get_commits_since_sha_exclusive(self, sha_last_update, branch_name="master"):
        commits = []
        commits_object = self.__repo_object.get_commits(branch_name)

        for commit in commits_object:
            if commit.sha == sha_last_update:
                break
            commits.append(self.get_commit(sha=commit.sha))

        commits.reverse()
        return commits

    def get_commit(self, branch_name="master", sha=None):
        if sha:
            commit = self.__repo_object.get_commit(sha)
        else:
            commit = self.__repo_object.get_branch(branch_name).commit

        return GithubCommit(commit)

    def post_pull_request_comment(self, issue_number, comment_text):
        self.__repo_object.get_pull(issue_number).create_issue_comment(comment_text)

    def post_commit_comment(self, sha, comment_text):
        self.__repo_object.get_commit(sha).create_comment(comment_text)

    def get_pull_request_files(self, issue_number):
        return [GithubCommitFile(file.filename, None, file.patch, file.status == "removed") for file in self.__repo_object.get_pull(issue_number).get_files()]

    def __get_file_object(self, filename):
        try:
            return self.__repo_object.get_contents(filename)
        except UnknownObjectException:
            print("File " + filename + " not found in " + self.full_name)

    def __load_github_repo(self):
        return GithubDirectory(self.__repo_object)

    def __file_path_to_list(self, path):
        return list(filter(None, path.split("/")))

    def __initialiase_owner(self):
        return {
            "type": self.__repo_object.owner.type
        }
