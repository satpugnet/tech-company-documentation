from github import UnknownObjectException

from github_interface.github_types.abstract_github_fs_node import AbstractGithubFSNode
from github_interface.github_types.factory.github_fs_node_factory import GithubFSNodeFactory
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

    def get_all_files_flat(self):
        file_system_nodes = []

        contents = self.__repo_object.get_contents("")
        while contents:
            content = contents.pop(0)
            if content.type == "dir":
                contents.extend(self.__repo_object.get_contents(content.path))
            else:
                file_system_nodes.append(GithubFSNodeFactory().create_from_github_get_contents(content))

        return file_system_nodes

    # TODO: separate the pure data part (like GithubFile...), the logic part and the github_interface_part
    def get_content_at_path(self, path=""):
        contents = self.__repo_object.get_contents(path)
        return GithubFSNodeFactory().create_from_github_get_contents(contents)

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

    # TODO: The response of /repos/:owner/:repo/pulls/:pull_number/files return a maximum of 300 files
    def get_pull_request_files(self, issue_number):
        return [GithubCommitFile(file.filename, None, file.patch, file.status == "removed") for file in self.__repo_object.get_pull(issue_number).get_files()]

    def __load_github_repo(self):
        # return GithubDirectory(self.__repo_object)
        return None

    def __file_path_to_list(self, path):
        return list(filter(None, path.split("/")))

    def __initialiase_owner(self):
        return {
            "type": self.__repo_object.owner.type
        }
