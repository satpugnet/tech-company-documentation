from github_interface.models.wrappers.abstract_github_fs_node import AbstractGithubFSNode
from utils.json.sensitive_jsonable import SensitiveJsonable


class GithubFile(AbstractGithubFSNode, SensitiveJsonable):
    def __init__(self, path, type, content):
        AbstractGithubFSNode.__init__(self, path, type)
        self.__content = content

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, new_content):
        self.__content = new_content

    def non_sensitive_data_to_json(self):
        new_json = {
            "content": self.content
        }
        return {**super().non_sensitive_data_to_json(), **new_json}
