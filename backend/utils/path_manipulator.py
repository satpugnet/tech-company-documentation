class PathManipulator:
    def dissociate_dir_path_from_fs_node_name(self, path):
        dir_path = path[:path.rfind('/') + 1] if path.rfind('/') != -1 else ""
        fs_node_name = path[path.rfind('/') + 1:] if path.rfind('/') != -1 else path
        return {
            "dir_path": dir_path,
            "fs_node_name": fs_node_name
        }
