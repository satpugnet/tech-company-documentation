from github import UnknownObjectException

from github_interface.types.github_file import GithubFile


# TODO: make it a @data class by giving all parameter in constructor
class GithubRepository:
    def __init__(self, repo_object):
        self.__repo_object = repo_object

    def get_full_name(self):
        return self.__repo_object.full_name

    def get_root_files(self):
        files = []
        contents = self.__repo_object.get_contents("")
        for content_file in contents:
            files.append(GithubFile(content_file))
        return files

    def get_file(self, file_name):
        try:
            return GithubFile(self.__repo_object.get_contents(file_name))
        except UnknownObjectException:
            print("File " + file_name + " not found in " + self.get_full_name())

    def get_commit_files(self, branch_name="master", sha=None):
        if sha:
            commit = self.__repo_object.get_commit(sha)
        else:
            commit = self.__repo_object.get_branch(branch_name).commit
        commit_filenames = [file.filename for file in commit.files]

        files = []
        for filename in commit_filenames:
            files.append(self.get_file(filename))

        return files



