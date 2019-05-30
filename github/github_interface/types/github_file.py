import base64

from github import GithubException


# TODO: make it a @data class by giving all parameter in constructor

class GithubFile:
    def __init__(self, file_object):
        self.__file_object = file_object
        self.__path = file_object.path
        self.__content = self.__decode_content(file_object) if self.__decode_content(file_object) else ""
        self.__lines = self.__content.splitlines()

    def get_path(self):
        return self.__path

    def get_content(self):
        return self.__content

    def get_type(self):
        return self.__file_object.type

    def get_lines(self, start=None, stop=None):
        start = start if start else 1
        stop = stop if stop else len(self.__lines)
        return self.__lines[start - 1:stop]

    def __decode_content(self, encoded_content):
        try:
            if (encoded_content.content):
                return base64.b64decode(encoded_content.content).decode('utf-8')
        except GithubException as e:
            print("Encoded content " + str(encoded_content) + " faced exception: " + str(e))
