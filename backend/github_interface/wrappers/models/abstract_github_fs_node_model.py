from abc import ABC, abstractmethod

from mongo.constants.model_fields import ModelFields
from tools.json.jsonable import Jsonable
from utils.path_manipulator import PathManipulator


class AbstractGithubFSNode(Jsonable, ABC):

    DIRECTORY_TYPE = "dir"
    FILE_TYPE = "file"

    PATH_FIELD = ModelFields.PATH
    TYPE_FIELD = ModelFields.TYPE
    NAME_FIELD = ModelFields.NAME
    DIR_PATH_FIELD = ModelFields.DIR_PATH

    def __init__(self, path="", type=DIRECTORY_TYPE):
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
        return PathManipulator().dissociate_dir_path_from_fs_node_name(path).fs_node_name

    def __extract_dir_path(self, path):
        return PathManipulator().dissociate_dir_path_from_fs_node_name(path).dir_path

    @abstractmethod
    def to_json(self):
        return {
            AbstractGithubFSNode.PATH_FIELD: self.path,
            AbstractGithubFSNode.TYPE_FIELD: self.type,
            AbstractGithubFSNode.NAME_FIELD: self.name,
            AbstractGithubFSNode.DIR_PATH_FIELD: self.dir_path
        }

