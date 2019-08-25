from enum import Enum


class GithubEventValues(Enum):
    """
    The different type of webhook events.
    """

    PUSH = "push"
    PULL_REQUEST = "pull_request"
    INSTALLATION = "installation"
