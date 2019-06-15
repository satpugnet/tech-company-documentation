from github import UnknownObjectException

from github_interface.github_types.github_commit_file import GithubCommitFile
from github_interface.github_types.github_directory import GithubDirectory


class GithubRepository:
    def __init__(self, repo_object):
        self.__repo_object = repo_object

    def get_full_name(self):
        return self.__repo_object.full_name

    def get_root_files(self):
        return GithubDirectory(self.__repo_object)

    def get_content_at_path(self, path=""):
        return GithubDirectory(self.__repo_object).get_content_at_path(path)

    def get_commit_files(self, branch_name="master", sha=None):
        if sha:
            commit = self.__repo_object.get_commit(sha)
        else:
            commit = self.__repo_object.get_branch(branch_name).commit

        files = []
        for file in commit.files:
            files.append(GithubCommitFile(self.__get_file_object(file.filename), file.previous_filename, file.patch))

        return files

    def __get_file_object(self, filename):
        try:
            return self.__repo_object.get_contents(filename)
        except UnknownObjectException:
            print("File " + filename + " not found in " + self.get_full_name())



