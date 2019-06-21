from github.GithubException import GithubException

from github_interface.github_types.abstract_github_file import AbstractGithubFile
from utils.json.jsonable import Jsonable


class GithubFile(AbstractGithubFile, Jsonable):
    def __init__(self, content_file):
        AbstractGithubFile.__init__(self, content_file)
        self._content = self.__get_decoded_content(content_file)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content):
        self._content = new_content

    def __get_decoded_content(self, file_object):
        try:
            if not file_object:
                return ""
            return file_object.decoded_content.decode("utf-8")
        except GithubException:
            return "File is too large to be displayed (>1 MB in size)"
        except UnicodeDecodeError:
            return "Error decoding, 'utf-8' codec cannot decode"

    def to_json(self):
        new_json = {
            "content": self.content
        }
        return {**super().to_json(), **new_json}
