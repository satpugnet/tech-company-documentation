class PathManipulator:
    """
    A wrapper around path regex manipulation.
    """

    def dissociate_dir_path_from_fs_node_name(self, path):
        """
        :return: A split path in 2 parts, the dir_path and the fs_node_name.
        (i.e. 'path/to/the/file.py -> 'path/to/the/' + file.py).
        """

        dir_path = path[:path.rfind('/') + 1] if path.rfind('/') != -1 else "/"
        fs_node_name = path[path.rfind('/') + 1:] if path.rfind('/') != -1 else path

        return PathManipulator.SplitPath(dir_path, fs_node_name)

    class SplitPath:

        def __init__(self, dir_path, fs_node_name):
            self._dir_path = dir_path
            self._fs_node_name = fs_node_name

        @property
        def dir_path(self):
            return self._dir_path

        @property
        def fs_node_name(self):
            return self._fs_node_name
