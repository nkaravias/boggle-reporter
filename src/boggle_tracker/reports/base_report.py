from abc import ABC, abstractmethod
from typing import List
from boggle_tracker.models.portfolio import Portfolio
from boggle_tracker.outputs.base_output import BaseOutput


class BaseReport(ABC):
    def __init__(self, portfolios: List[Portfolio], output: BaseOutput):
        self.portfolios = portfolios
        self.output = output

    @abstractmethod
    def generate(self):
        pass
