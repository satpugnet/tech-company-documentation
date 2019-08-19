from abc import ABC, abstractmethod


class SensitiveJsonable(ABC):
    @abstractmethod
    def non_sensitive_data_to_json(self):
        pass
