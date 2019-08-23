from abc import ABC, abstractmethod


class Jsonable(ABC):

    @abstractmethod
    def to_json(self):
        pass
