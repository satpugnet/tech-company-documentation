from github import GithubException

from github_interface.models.wrappers.abstract_github_fs_node import AbstractGithubFSNode
from github_interface.models.wrappers.github_directory import GithubDirectory
from github_interface.models.wrappers.github_file import GithubFile
from utils.path_manipulator import PathManipulator


class GithubFSNodeFactory:
    """
    see https://developer.github.com/v3/repos/contents/
    """

    def create_from_github_get_contents(self, raw_fs_node):
        if isinstance(raw_fs_node, list):
            raw_fs_node = self.__GithubDirectoryFactory().create_github_dir_from_github_get_contents(raw_fs_node)
        elif raw_fs_node.type == "file":
            raw_fs_node = self.__GithubFileFactory().create_github_file_from_github_get_contents(raw_fs_node)
        else:
            raise("This content type is not currently supported by the factories: " + str(raw_fs_node.type))

        return raw_fs_node

    def _create_from_github_get_contents_sub_fs_nodes(self, raw_fs_node):
        if raw_fs_node.type == "dir":
            fs_node = self.__GithubDirectoryFactory().create_github_dir_without_sub_fs_nodes_from_github_get_contents(raw_fs_node)
        else:
            fs_node = self.create_from_github_get_contents(raw_fs_node)

        return fs_node

    class __GithubDirectoryFactory:
        def create_github_dir_from_github_get_contents(self, raw_dirs):
            return GithubDirectory(self.__extract_path_to_dir(raw_dirs[0].path), AbstractGithubFSNode.DIRECTORY,
                                   self.__extract_sub_fs_nodes(raw_dirs))

        def create_github_dir_without_sub_fs_nodes_from_github_get_contents(self, raw_fs_node):
            return GithubDirectory(raw_fs_node.path, AbstractGithubFSNode.DIRECTORY)

        def __extract_path_to_dir(self, sub_fs_node_path):
            return PathManipulator().dissociate_dir_path_from_fs_node_name(sub_fs_node_path).dir_path

        def __extract_sub_fs_nodes(self, raw_dirs):
            return [GithubFSNodeFactory()._create_from_github_get_contents_sub_fs_nodes(raw_fs_node) for raw_fs_node in raw_dirs]

    class __GithubFileFactory:
        def create_github_file_from_github_get_contents(self, raw_file):
            return GithubFile(raw_file.path, AbstractGithubFSNode.FILE, self.__extract_decoded_content(raw_file))

        def __extract_decoded_content(self, raw_file):
            try:
                if not raw_file:
                    return ""
                return raw_file.decoded_content.decode("utf-8")
            except GithubException:
                return "File is too large to be displayed (>1 MB in size)"
            except UnicodeDecodeError:
                return "Error decoding, 'utf-8' codec cannot decode"
            except AssertionError:
                return "Unsupported encoding"


