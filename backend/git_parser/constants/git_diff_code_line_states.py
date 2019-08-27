from enum import Enum


class GitDiffCodeLineStates(Enum):
    """
    An enum for the state of a code line in a patch.
    """

    UNCHANGED = 1
    ADDED = 2
    REMOVED = 3
