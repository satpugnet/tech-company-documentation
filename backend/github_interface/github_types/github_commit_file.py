from github_interface.git.git_diff_parser import GitDiffParser
from github_interface.github_types.github_file import GithubFile


class GithubCommitFile(GithubFile):
    def __init__(self, content_file, path, previous_path, patch, is_deleted):
        GithubFile.__init__(self, content_file)
        self.__path = path
        self.__has_path_changed = not (previous_path is None)
        self.__previous_path = self.__path if previous_path is None else previous_path
        self.__git_diff_parser = GitDiffParser(patch)
        self.__is_deleted = is_deleted

    @property
    def previous_path(self):
        return self.__previous_path

    @property
    def has_path_changed(self):
        return self.__has_path_changed

    @property
    def is_deleted(self):
        return self.__is_deleted

    def calculate_updated_line_range(self, start_line, end_line):
        return self.__git_diff_parser.calculate_updated_line_range(start_line, end_line)

    def to_json(self):
        new_json = {
            "previous_path": self.previous_path
        }
        return {**super().to_json(), **new_json}

