from typing import List
from boggle_tracker.models.portfolio import Portfolio
from boggle_tracker.outputs.base_output import BaseOutput
from boggle_tracker.reports.base_report import BaseReport
from boggle_tracker.reports.generic_portfolio_overview_report import (
    GenericPortfolioOverviewReport,
)


class ReportFactory:
    @staticmethod
    def create(report_type: str, portfolios: List[Portfolio], output: BaseOutput) -> BaseReport:
        if report_type == 'generic_overview':
            return GenericPortfolioOverviewReport(portfolios, output)
        else:
            raise ValueError(f"Unsupported report type: {report_type}")
