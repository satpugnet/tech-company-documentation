from github_interface.wrappers.models.abstract_github_fs_node_model import AbstractGithubFSNode
from mongo.constants.model_fields import ModelFields

from tools.json.jsonable import Jsonable


class GithubFileModel(AbstractGithubFSNode, Jsonable):
    """
    Represent a github file.
    """

    CONTENT_FIELD = ModelFields.CONTENT

    def __init__(self, path, type, content):
        AbstractGithubFSNode.__init__(self, path, type)
        self.__content = content

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, new_content):
        self.__content = new_content

    def to_json(self):
        new_json = {
            GithubFileModel.CONTENT_FIELD: self.content
        }
        return {**super().to_json(), **new_json}
