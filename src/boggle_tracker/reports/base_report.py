from abc import ABC, abstractmethod


class BaseReport(ABC):
    @abstractmethod
    def generate_data(self):
        pass

    @abstractmethod
    def get_report_type(self):
        pass
