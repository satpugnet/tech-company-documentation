from mongo.constants.db_fields import ModelFields
from utils.json.sensitive_jsonable import SensitiveJsonable
from utils.path_manipulator import PathManipulator


class AbstractGithubFSNode(SensitiveJsonable):

    DIRECTORY_TYPE = "dir"
    FILE_TYPE = "file"

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

    def non_sensitive_data_to_json(self):
        return {
            ModelFields.PATH: self.path,
            ModelFields.TYPE: self.type,
            ModelFields.NAME: self.name,
            ModelFields.DIR_PATH: self.dir_path
        }

