import re

from github_interface.git.git_diff_types.git_diff_code_line import GitDiffCodeLine
from github_interface.git.git_diff_types.git_diff_code_line_state import GitDiffCodeLineState
from github_interface.git.git_diff_types.git_diff_constant import GitDiffConstant


class GitDiffHunk:
    def __init__(self, raw_hunk):
        match = re.search(GitDiffConstant.HUNK_HEADING_REGEX, raw_hunk)
        if raw_hunk[match.end()] != '\n':
            raw_hunk = raw_hunk[:match.end()] + '\n' + raw_hunk[match.end():]

        raw_hunk_lines = raw_hunk.splitlines()
        heading_search = re.search(GitDiffConstant.HUNK_HEADING_REGEX, raw_hunk_lines[0])
        self.old_start_line = heading_search.group(1)
        self.old_length = heading_search.group(2)
        self.new_start_line = heading_search.group(3)
        self.new_length = heading_search.group(4)

        self.code_lines = list(map(self.__convert_to_code_line, raw_hunk_lines[1:]))

    def get_old_start_line(self):
        return int(self.old_start_line)

    def get_old_length(self):
        return int(self.old_length)

    def get_new_start_line(self):
        return int(self.new_start_line)

    def get_new_length(self):
        return int(self.new_length)

    def get_code_lines(self):
        return self.code_lines

    def count_line_change_before_inclusive(self, line_number):
        return self.__count_line_change_helper(line_number, True)

    def count_line_change_after_exclusive(self, line_number):
        return self.__count_line_change_helper(line_number, False)

    # TODO: check what happen if the end (or beginning) is replaced and whether after a REMOVED on the line_number, we should keep looking for addition after
    def __count_line_change_helper(self, line_number, is_count_before):
        current_old_line_number = self.get_old_start_line() - 1
        total_line_change = 0
        counter_reseted = False

        for code_line in self.code_lines:
            if code_line.state == GitDiffCodeLineState.UNCHANGED:
                current_old_line_number += 1
            elif code_line.state == GitDiffCodeLineState.REMOVED:
                current_old_line_number += 1
                total_line_change -= 1
            elif code_line.state == GitDiffCodeLineState.ADDED:
                total_line_change += 1

            if current_old_line_number == line_number and not counter_reseted:
                if is_count_before:
                    break
                else:
                    counter_reseted = True
                    total_line_change = 0

        return total_line_change


    def __convert_to_code_line(self, raw_hunk_line):
        code_line_state = GitDiffCodeLineState.UNCHANGED
        if raw_hunk_line[0] == '-':
            code_line_state = GitDiffCodeLineState.REMOVED
        elif raw_hunk_line[0] == '+':
            code_line_state = GitDiffCodeLineState.ADDED

        return GitDiffCodeLine(raw_hunk_line[1:], code_line_state)



