from enum import Enum


class GitDiffCodeLineStates(Enum):
    UNCHANGED = 1
    ADDED = 2
    REMOVED = 3
