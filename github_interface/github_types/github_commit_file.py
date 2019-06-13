from git.git_diff_parser import GitDiffParser
from github_types.github_file import GithubFile


class GithubCommitFile(GithubFile):
    def __init__(self, content_file, previous_path, patch):
        GithubFile.__init__(self, content_file)
        self.__previous_path = previous_path
        self.git_diff_parser = GitDiffParser(patch)

    def calculate_updated_line_range(self, start_line, end_line):
        return self.git_diff_parser.calculate_updated_line_range(start_line, end_line)

    def get_previous_path(self):
        return self.__previous_path

    def has_path_changed(self):
        return self.__previous_path != None

