from abc import ABC, abstractmethod


class AbstractRequestHandler(ABC):
    """
    Abstract request handler for the webhook.
    """

    @abstractmethod
    def enact(self):
        pass
