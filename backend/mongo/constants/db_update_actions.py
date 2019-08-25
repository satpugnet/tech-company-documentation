from enum import Enum


class DbUpdateActions(Enum):
    """
    An enum of all the update possible actions.
    """

    INC_ACTION = "inc"
    SET_ACTION = "set"
