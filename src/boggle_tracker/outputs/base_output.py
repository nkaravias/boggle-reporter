from abc import ABC, abstractmethod


class BaseOutput(ABC):
    @abstractmethod
    def output(self, content: str):
        pass