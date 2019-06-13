from enum import Enum


class GitDiffCodeLineState(Enum):
    UNCHANGED = 1
    ADDED = 2
    REMOVED = 3
