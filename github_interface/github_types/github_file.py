import base64

from github import GithubException

from github_types.abstract_github_file import AbstractGithubFile


class GithubFile(AbstractGithubFile):
    def __init__(self, content_file):
        AbstractGithubFile.__init__(self, content_file)
        self.__content = self.__decode_content(content_file) if self.__decode_content(content_file) else ""
        self.__lines = self.__content.splitlines()

    def get_content(self):
        return self.__content

    def get_lines(self, start=None, stop=None):
        start = start if start else 1
        stop = stop if stop else len(self.__lines)
        return self.__lines[start - 1:stop]

    def __decode_content(self, content_file):
        try:
            if (content_file and content_file.content):
                return base64.b64decode(content_file.content)
        except GithubException as e:
            print("Encoded content " + str(content_file) + " faced exception: " + str(e))
