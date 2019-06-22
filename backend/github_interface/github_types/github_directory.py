from github import UnknownObjectException

from github_interface.github_types.abstract_github_file import AbstractGithubFile
from github_interface.github_types.github_file import GithubFile
from utils.json.jsonable import Jsonable


class GithubDirectory(AbstractGithubFile, Jsonable):

    def __init__(self, repo_object, content_file=""):
        AbstractGithubFile.__init__(self, content_file)
        print("Downloading directory: /" + str(self.path))
        self.__repo_object = repo_object
        self._subfiles = None

    @property
    def subfiles(self):
        return self._subfiles

    def load_subfiles(self):
        if self.subfiles:
            self._subfiles = self.subfiles
        else:
            self._subfiles = self.__initialise_subfiles()
        return self.subfiles

    def __initialise_subfiles(self):
        files = {}
        contents = self.__repo_object.get_contents(self.path)
        for content_file in contents:
            # Submodule type are currently breaking here
            if content_file.type == AbstractGithubFile.DIRECTORY:
                files[content_file.name] = GithubDirectory(self.__repo_object, content_file)
            else:
                files[content_file.name] = GithubFile(content_file)
        return files

    def __get_file_object(self, filename):
        try:
            return self.__repo_object.get_contents(filename)
        except UnknownObjectException:
            print("File " + filename + " not found")

    def to_json(self):
        new_json = {
            "subfiles": self.subfiles
        }
        return {**super().to_json(), **new_json}

