from github import GithubException

from github_interface.github_types.abstract_github_fs_node import AbstractGithubFSNode
from github_interface.github_types.github_directory import GithubDirectory
from github_interface.github_types.github_file import GithubFile
from utils.path_manipulator import PathManipulator


class GithubFSNodeFactory:

    """
    see https://developer.github.com/v3/repos/contents/
    """
    def create_from_github_get_contents(self, fs_node):
        if isinstance(fs_node, list):
            fs_node = self.__GithubDirectoryFactory().create_github_dir_from_github_get_contents(fs_node)
        elif fs_node.type == "file":
            fs_node = self.__GithubFileFactory().create_github_file_from_github_get_contents(fs_node)
        else:
            raise("This content type is not currently supported by the factory: " + str(fs_node.type))

        return fs_node

    def _create_from_github_get_contents_sub_fs_nodes(self, fs_node):
        if fs_node.type == "dir":
            fs_node = self.__GithubDirectoryFactory().create_github_dir_without_sub_fs_nodes_from_github_get_contents(fs_node)
        else:
            fs_node = self.create_from_github_get_contents(fs_node)
        return fs_node

    class __GithubDirectoryFactory:

        def create_github_dir_from_github_get_contents(self, fs_nodes):
            return GithubDirectory(self.__extract_path_to_dir(fs_nodes[0].path), AbstractGithubFSNode.DIRECTORY, self.__extract_sub_fs_nodes(fs_nodes))

        def create_github_dir_without_sub_fs_nodes_from_github_get_contents(self, fs_node):
            return GithubDirectory(fs_node.path, AbstractGithubFSNode.DIRECTORY)

        def __extract_path_to_dir(self, sub_fs_node_path):
            return PathManipulator().dissociate_dir_path_from_fs_node_name(sub_fs_node_path)["dir_path"]

        def __extract_sub_fs_nodes(self, fs_nodes):
            return [GithubFSNodeFactory()._create_from_github_get_contents_sub_fs_nodes(fs_node) for fs_node in fs_nodes]

    class __GithubFileFactory:

        def create_github_file_from_github_get_contents(self, file):
            return GithubFile(file.path, AbstractGithubFSNode.FILE, self.__extract_decoded_content(file))

        def __extract_decoded_content(self, file):
            try:
                if not file:
                    return ""
                return file.decoded_content.decode("utf-8")
            except GithubException:
                return "File is too large to be displayed (>1 MB in size)"
            except UnicodeDecodeError:
                return "Error decoding, 'utf-8' codec cannot decode"
            except AssertionError:
                return "Unsupported encoding"


