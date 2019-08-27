from abc import ABC, abstractmethod


class AbstractWebhookAction(ABC):
    """
    Abstract class serving as an interface for an action. An action is an atomic single task executed by one of the
    webhook request handlers. They are used to enforce clear distinction of the task performed upon a webhook request
    reception.
    """

    @abstractmethod
    def perform(self):
        pass
