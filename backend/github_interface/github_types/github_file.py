import base64

from github.GithubException import GithubException

from github_interface.github_types.abstract_github_file import AbstractGithubFile


class GithubFile(AbstractGithubFile):
    def __init__(self, content_file):
        AbstractGithubFile.__init__(self, content_file)
        self.__content = self.__get_decoded_content(content_file)
        self.__lines = self.__content.splitlines()

    def get_content(self):
        return self.__content

    def get_lines(self, start=None, stop=None):
        start = start if start else 1
        stop = stop if stop else len(self.__lines)
        return self.__lines[start - 1:stop]

    def __get_decoded_content(self, file_object):
        try:
            return file_object.decoded_content
        except GithubException:
            return "File is too large to be displayed (>1 MB in size)"
