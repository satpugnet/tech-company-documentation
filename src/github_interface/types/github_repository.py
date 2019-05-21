from github import UnknownObjectException

from github_interface.types.github_file import GithubFile


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

