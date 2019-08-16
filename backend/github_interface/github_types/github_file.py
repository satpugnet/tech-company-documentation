from github_interface.github_types.abstract_github_fs_node import AbstractGithubFSNode
from utils.json.jsonable import Jsonable


class GithubFile(AbstractGithubFSNode, Jsonable):
    def __init__(self, path, type, content):
        AbstractGithubFSNode.__init__(self, path, type)
        self._content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content):
        self._content = new_content

    def to_json(self):
        new_json = {
            "content": self.content
        }
        return {**super().to_json(), **new_json}
