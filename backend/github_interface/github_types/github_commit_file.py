from github_interface.git.git_diff_parser import GitDiffParser
from github_interface.github_types.github_file import GithubFile


class GithubCommitFile(GithubFile):
    def __init__(self, content_file, previous_path, patch):
        GithubFile.__init__(self, content_file)
        self._previous_path = previous_path
        self.__git_diff_parser = GitDiffParser(patch)

    @property
    def previous_path(self):
        return self._previous_path

    def calculate_updated_line_range(self, start_line, end_line):
        return self.__git_diff_parser.calculate_updated_line_range(start_line, end_line)

    def has_path_changed(self):
        return self.previous_path is not None

    def to_json(self):
        new_json = {
            "previous_path": self.previous_path
        }
        return {**super().to_json(), **new_json}

