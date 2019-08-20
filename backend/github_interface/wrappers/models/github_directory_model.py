from github_interface.wrappers.models.abstract_github_fs_node_model import AbstractGithubFSNode
from mongo.constants.db_fields import ModelFields
from utils.json.sensitive_jsonable import SensitiveJsonable


class GithubDirectoryModel(AbstractGithubFSNode, SensitiveJsonable):

    def __init__(self, path, type, sub_fs_nodes=None):
        AbstractGithubFSNode.__init__(self, path, type)
        self.__sub_fs_nodes = sub_fs_nodes
        self.__is_initialised = sub_fs_nodes is not None

    @property
    def sub_fs_nodes(self):
        if not self.__is_initialised:
            raise Exception("The content of this directory was not initialised")
        return self.__sub_fs_nodes

    @property
    def is_initialised(self):
        return self.__is_initialised

    def non_sensitive_data_to_json(self):
        new_json = {}
        if self.is_initialised:
            new_json = {
                ModelFields.SUB_FS_NODES: self.sub_fs_nodes
            }

        return {**super().non_sensitive_data_to_json(), **new_json}
