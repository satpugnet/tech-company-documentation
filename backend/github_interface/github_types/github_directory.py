from github_interface.github_types.abstract_github_fs_node import AbstractGithubFSNode
from utils.json.jsonable import Jsonable


class GithubDirectory(AbstractGithubFSNode, Jsonable):

    def __init__(self, path, type, sub_fs_nodes=None):
        AbstractGithubFSNode.__init__(self, path, type)
        self._sub_fs_nodes = sub_fs_nodes

    @property
    def sub_fs_nodes(self):
        if self._sub_fs_nodes is None:
            raise Exception("The content of this directory was not initialised")
        return self._sub_fs_nodes

    def to_json(self):
        try:
            new_json = {
                "sub_fs_nodes": self.sub_fs_nodes
            }
        except:
            new_json = {}

        return {**super().to_json(), **new_json}
