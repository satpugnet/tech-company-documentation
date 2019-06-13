from git.git_diff_parser import GitDiffParser
from github_types.github_file import GithubFile


class GithubCommitFile(GithubFile):
    def __init__(self, file_object, patch):
        GithubFile.__init__(self, file_object)
        self.patch = patch
        self.git_diff_parser = GitDiffParser(patch)

    def get_patch(self):
        return self.patch

    def calculate_updated_line_range(self, start_line, end_line):
        return self.git_diff_parser.calculate_updated_line_range(start_line, end_line)

