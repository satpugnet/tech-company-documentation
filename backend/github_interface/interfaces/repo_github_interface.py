from github_interface.wrappers.factories.github_fs_node_factory import GithubFSNodeFactory
from github_interface.wrappers.models.git_commit_model import GithubCommitModel
from github_interface.wrappers.models.github_commit_file_model import GithubCommitFileModel
from github_interface.wrappers.models.github_repo_model import GithubRepoModel


class RepoGithubInterface:
    def __init__(self, raw_repo):
        self.__repo_object = raw_repo
        self.__repo = GithubRepoModel(raw_repo.owner.login, raw_repo.name, raw_repo.full_name, raw_repo.owner.type, bool(raw_repo.private))

    @property
    def repo(self):
        return self.__repo

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

    def get_fs_node_at_path(self, path=""):
        contents = self.__repo_object.get_contents(path)
        return GithubFSNodeFactory().create_from_github_get_contents(contents)

    def get_commits_since_sha_exclusive(self, sha_last_update, branch_name="master"):
        raw_commits = self.__repo_object.get_commits(branch_name)

        commits = []
        for commit in raw_commits:
            if commit.sha == sha_last_update:
                break
            commits.append(self.get_commit(sha=commit.sha))

        commits.reverse()
        return commits

    def get_commit(self, branch_name="master", sha=None):
        if sha:
            raw_commit = self.__repo_object.get_commit(sha)
        else:
            raw_commit = self.__repo_object.get_branch(branch_name).commit

        commit_files = []
        for file in raw_commit.files:
            commit_files.append(GithubCommitFileModel(file.filename, file.previous_filename, file.patch, file.status == "removed"))

        return GithubCommitModel(commit_files, raw_commit.sha)

    def post_pull_request_comment(self, issue_number, comment_text):
        self.__repo_object.get_pull(issue_number).create_issue_comment(comment_text)

    def post_commit_comment(self, sha, comment_text):
        self.__repo_object.get_commit(sha).create_comment(comment_text)

    def get_pull_request_files(self, issue_number):
        """
        TODO: The response of /repos/:owner/:repo/pulls/:pull_number/files is a maximum of 300 files, a way around this needs to be implemented
        :param issue_number: The issue number associated with the pull_request (issue number and pull request number are the same in Github).
        :return: A list of GithubCommitFile.
        """
        pr_files = self.__repo_object.get_pull(issue_number).get_files()
        return [GithubCommitFileModel(file.filename, None, file.patch, file.status == "removed") for file in pr_files]
