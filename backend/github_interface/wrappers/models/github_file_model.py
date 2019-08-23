from github_interface.wrappers.models.abstract_github_fs_node_model import AbstractGithubFSNode
from mongo.constants.model_fields import ModelFields
from tools.json.sensitive_jsonable import SensitiveJsonable


class GithubFileModel(AbstractGithubFSNode, SensitiveJsonable):

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

    def non_sensitive_data_to_json(self):
        new_json = {
            GithubFileModel.CONTENT_FIELD: self.content
        }
        return {**super().non_sensitive_data_to_json(), **new_json}
