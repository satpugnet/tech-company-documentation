import base64

from github import GithubException

from github_interface.github_types.abstract_github_file import AbstractGithubFile


class GithubFile(AbstractGithubFile):
    def __init__(self, file_object):
        AbstractGithubFile.__init__(self, file_object.path, file_object.type)
        self.__content = self.__decode_content(file_object) if self.__decode_content(file_object) else ""
        self.__lines = self.__content.splitlines()

    def get_content(self):
        return self.__content

    def get_lines(self, start=None, stop=None):
        start = start if start else 1
        stop = stop if stop else len(self.__lines)
        return self.__lines[start - 1:stop]

    def __decode_content(self, encoded_content):
        try:
            if (encoded_content.content):
                return base64.b64decode(encoded_content.content)
        except GithubException as e:
            print("Encoded content " + str(encoded_content) + " faced exception: " + str(e))
