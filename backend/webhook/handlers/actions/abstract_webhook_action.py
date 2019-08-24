from abc import ABC, abstractmethod


class AbstractWebhookAction(ABC):

    @abstractmethod
    def perform(self):
        pass
