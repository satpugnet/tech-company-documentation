from abc import ABC, abstractmethod


class AbstractRequestHandler(ABC):

    @abstractmethod
    def enact(self):
        pass
