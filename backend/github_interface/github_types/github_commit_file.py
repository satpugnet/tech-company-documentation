from github_interface.git.git_diff_parser import GitDiffParser


class GithubCommitFile:
    def __init__(self, path, previous_path, patch, is_deleted):
        self._path = path
        self._has_path_changed = not (previous_path is None)
        self._previous_path = self._path if previous_path is None else previous_path
        self.__git_diff_parser = GitDiffParser(patch)
        self._is_deleted = is_deleted

    @property
    def path(self):
        return self._path

    @property
    def previous_path(self):
        return self._previous_path

    @property
    def has_path_changed(self):
        return self._has_path_changed

    @property
    def is_deleted(self):
        return self._is_deleted

    def calculate_updated_line_range(self, start_line, end_line):
        return self.__git_diff_parser.calculate_updated_line_range(start_line, end_line)

    def to_json(self):
        new_json = {
            "previous_path": self.previous_path
        }
        return {**super().to_json(), **new_json}

