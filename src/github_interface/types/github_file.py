import base64

from github import GithubException


class GithubFile:
    def __init__(self, file_object):
        self.__file_object = file_object

    def get_content(self):
        return self.__decode_content(self.__file_object)

    def get_type(self):
        return self.__file_object.type

    def __decode_content(self, encoded_content):
        try:
            if (encoded_content.content):
                return base64.b64decode(encoded_content.content)
        except GithubException as e:
            print("Encoded content " + str(encoded_content) + " faced exception: " + str(e))
