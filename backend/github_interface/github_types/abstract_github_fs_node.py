from utils.json.jsonable import Jsonable
from utils.path_manipulator import PathManipulator


class AbstractGithubFSNode(Jsonable):

    DIRECTORY = "dir"
    FILE = "file"

    def __init__(self, path="", type=DIRECTORY):
        self._path = path
        self._type = type
        self._name = self.__extract_fs_node_name(self._path)
        self._dir_path = self.__extract_dir_path(self._path)

    @property
    def path(self):
        return self._path

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def dir_path(self):
        return self._dir_path

    def __extract_fs_node_name(self, path):
        return PathManipulator().dissociate_dir_path_from_fs_node_name(path)["fs_node_name"]

    def __extract_dir_path(self, path):
        return PathManipulator().dissociate_dir_path_from_fs_node_name(path)["dir_path"]

    def to_json(self):
        return {
            "path": self.path,
            "type": self.type,
            "name": self.name,
            "dir_path": self.dir_path
        }

