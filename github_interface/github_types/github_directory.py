from github import UnknownObjectException

from github_types.abstract_github_file import AbstractGithubFile
from github_types.github_file import GithubFile


class GithubDirectory(AbstractGithubFile):

    DIRECTORY = "dir"

    def __init__(self, repo_object, content_file):
        AbstractGithubFile.__init__(self, content_file)
        self.__repo_object = repo_object

    def get_subfiles(self):
        files = {}
        contents = self.__repo_object.get_contents(self.get_path())
        for content_file in contents:
            if content_file.type == GithubDirectory.DIRECTORY:
                files[content_file.name] = GithubDirectory(self.__repo_object, content_file)
            else:
                files[content_file.name] = GithubFile(content_file)
        return files

    def __get_file_object(self, file_name):
        try:
            return self.__repo_object.get_contents(file_name)
        except UnknownObjectException:
            print("File " + file_name + " not found")

