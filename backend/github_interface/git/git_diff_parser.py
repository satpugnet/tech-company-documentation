import re

from github_interface.git.git_diff_types.git_diff_hunk import GitDiffHunk
from github_interface.git.git_diff_types.git_diff_constant import GitDiffConstant


class GitDiffParser:
    def __init__(self, file_raw_patch):
        self.hunks = self.__extract_hunks(file_raw_patch)

    def get_hunk(self):
        return self.hunks

    def calculate_updated_line_range(self, start_line, end_line):
        updated_start_line = start_line
        updated_end_line = end_line

        for hunk in self.hunks:
            if self.__is_hunk_before_line(hunk, start_line):
                updated_start_line += hunk.get_new_length() - hunk.get_old_length()
                updated_end_line += hunk.get_new_length() - hunk.get_old_length()
            elif self.__is_hunk_after_line(hunk, end_line):
                pass
            else:
                if self.__is_hunk_inside_line_range(hunk, start_line, end_line):
                    updated_end_line += hunk.get_new_length() - hunk.get_old_length()
                elif self.__is_hunk_overlapping_end(hunk, start_line, end_line):
                    updated_end_line += hunk.count_line_change_before_inclusive(end_line)
                elif self.__is_hunk_overlapping_start(hunk, start_line, end_line):
                    updated_start_line += hunk.count_line_change_before_inclusive(start_line)
                    updated_end_line += hunk.count_line_change_after_exclusive(start_line) + hunk.count_line_change_before_inclusive(start_line)

        return updated_start_line, updated_end_line

    def __extract_hunks(self, file_raw_patch):
        if not file_raw_patch:
            return []
        hunk_positions = [match.start() for match in re.finditer(GitDiffConstant.HUNK_HEADING_REGEX, file_raw_patch)]

        hunks = []
        for i in range(len(hunk_positions)):
            start_index = hunk_positions[i]
            end_index = len(file_raw_patch) if len(hunk_positions) == i + 1 else hunk_positions[i + 1]

            hunks.append(GitDiffHunk(file_raw_patch[start_index:end_index]))
        return hunks

    def __is_hunk_before_line(self, hunk, start_line):
        return self.__hunk_old_end_line(hunk) < start_line

    def __is_hunk_after_line(self, hunk, end_line):
        return end_line < hunk.get_old_start_line()

    def __is_hunk_inside_line_range(self, hunk, start_line, end_line):
        return hunk.get_old_start_line() > start_line and self.__hunk_old_end_line(hunk) < end_line

    def __is_hunk_overlapping_end(self, hunk, start_line, end_line):
        return hunk.get_old_start_line() > start_line and self.__hunk_old_end_line(hunk) >= end_line

    def __is_hunk_overlapping_start(self, hunk, start_line, end_line):
        return hunk.get_old_start_line() <= start_line and self.__hunk_old_end_line(hunk) < end_line

    def __hunk_old_end_line(self, hunk):
        return hunk.get_old_start_line() + hunk.get_old_length() - 1


