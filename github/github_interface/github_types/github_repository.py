from github import UnknownObjectException

from github_interface.github_types.github_commit_file import GithubCommitFile
from github_interface.github_types.github_directory import GithubDirectory
from github_interface.github_types.github_file import GithubFile


class GithubRepository:
    def __init__(self, repo_object):
        self.__repo_object = repo_object

    def get_full_name(self):
        return self.__repo_object.full_name

    def get_root_files(self):
        return GithubDirectory(self.__repo_object, "")

    def get_commit_files(self, branch_name="master", sha=None):
        if sha:
            commit = self.__repo_object.get_commit(sha)
        else:
            commit = self.__repo_object.get_branch(branch_name).commit

        files = []
        for file in commit.files:
            files.append(GithubCommitFile(self.__get_file_object(file.filename), file.patch))

        return files

    def __get_file_object(self, file_name):
        try:
            return self.__repo_object.get_contents(file_name)
        except UnknownObjectException:
            print("File " + file_name + " not found in " + self.get_full_name())



