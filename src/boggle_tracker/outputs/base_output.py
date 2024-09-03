from abc import ABC, abstractmethod


class BaseOutput(ABC):
    @abstractmethod
    def output(self, data: dict, report_type: str):
        pass
