from abc import ABC, abstractmethod


class Jsonable(ABC):
    """
    An interface for models that can be converted to json.
    """

    @abstractmethod
    def to_json(self):
        pass
