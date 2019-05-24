import base64

from github import GithubException


class GithubFile:
    def __init__(self, file_object):
        self.__file_object = file_object
        self.__content = self.__decode_content(file_object)
        self.__lines = self.__content.splitlines()

    def get_content(self):
        return self.__content

    def get_type(self):
        return self.__file_object.type

    def get_lines(self, start=None, stop=None):
        start = start if start else 0
        stop = stop if stop else len(self.__lines) - 1
        return self.__lines[start:stop+1]

    def __decode_content(self, encoded_content):
        try:
            if (encoded_content.content):
                return base64.b64decode(encoded_content.content).decode('utf-8')
        except GithubException as e:
            print("Encoded content " + str(encoded_content) + " faced exception: " + str(e))
