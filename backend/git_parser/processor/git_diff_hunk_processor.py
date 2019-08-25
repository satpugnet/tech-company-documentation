import re

from git_parser.constants.git_diff_code_line_states import GitDiffCodeLineStates
from git_parser.models.git_patch_code_line_model import GitPatchCodeLineModel
from tools import logger


class GitDiffHunk:
    """
    Represent a single hunk in a git patch, and computes useful properties about this hunk. It contains the original
    start and length as well as the new start and length of the hunk.
    """
    HUNK_HEADING_REGEX = "@@ -(\d+),(\d+) \\+(\d+),(\d+) @@"

    def __init__(self, raw_hunk):
        matched_heading = re.search(GitDiffHunk.HUNK_HEADING_REGEX, raw_hunk)
        if raw_hunk[matched_heading.end()] != '\n':
            raw_hunk = raw_hunk[:matched_heading.end()] + '\n' + raw_hunk[matched_heading.end():]
        raw_hunk_lines = raw_hunk.splitlines()
        heading_search = re.search(GitDiffHunk.HUNK_HEADING_REGEX, raw_hunk_lines[0])

        self.__old_start_line = int(heading_search.group(1))
        self.__old_length = int(heading_search.group(2))
        self.__new_start_line = int(heading_search.group(3))
        self.__new_length = int(heading_search.group(4))
        self.__code_lines = list(map(self.__convert_to_code_line, raw_hunk_lines[1:]))

    @property
    def old_start_line(self):
        return self.__old_start_line

    @property
    def old_length(self):
        return self.__old_length

    @property
    def new_start_line(self):
        return self.__new_start_line

    @property
    def new_length(self):
        return self.__new_length

    @property
    def code_lines(self):
        return self.__code_lines

    def count_line_changed_before_inclusive(self, line_number):
        return self.__count_line_changed_helper(line_number, True)

    def count_line_changed_after_exclusive(self, line_number):
        return self.__count_line_changed_helper(line_number, False)

    # TODO: check what happen if the end (or beginning) is replaced and whether after a REMOVED on the line_number,
    #  we should keep looking for addition after
    def __count_line_changed_helper(self, line_number, is_count_before_line):
        """
        Count the number of lines changed by the hunk.
        """
        current_old_line_number = int(self.old_start_line) - 1
        total_line_changed = 0
        counter_reseted = False

        for code_line in self.code_lines:
            if code_line.state == GitDiffCodeLineStates.UNCHANGED:
                current_old_line_number += 1

            elif code_line.state == GitDiffCodeLineStates.REMOVED:
                current_old_line_number += 1
                total_line_changed -= 1

            elif code_line.state == GitDiffCodeLineStates.ADDED:
                total_line_changed += 1

            if current_old_line_number == line_number and not counter_reseted:
                if is_count_before_line:
                    break
                else:
                    counter_reseted = True
                    total_line_changed = 0

        return total_line_changed

    def __convert_to_code_line(self, raw_hunk_line):
        """
        Computes the state of each code line in the given hunk and returns a GitDiffCodeLine object
        """
        code_line_state = GitDiffCodeLineStates.UNCHANGED

        if raw_hunk_line[0] == '-':
            code_line_state = GitDiffCodeLineStates.REMOVED

        elif raw_hunk_line[0] == '+':
            code_line_state = GitDiffCodeLineStates.ADDED

        return GitPatchCodeLineModel(raw_hunk_line[1:], code_line_state)



