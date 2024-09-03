from typing import List
from boggle_tracker.reports.base_report import BaseReport
from boggle_tracker.reports.generic_overview_report import GenericOverviewReport
from boggle_tracker.reports.target_allocation_report import TargetAllocationReport
from boggle_tracker.models.portfolio import Portfolio


class ReportFactory:
    @staticmethod
    def create(report_type: str, portfolios: List[Portfolio], **kwargs) -> BaseReport:
        if report_type == "generic_overview":
            return GenericOverviewReport(portfolios)
        elif report_type == "target_allocation":
            target_allocation = kwargs.get('target_allocation')
            if not target_allocation:
                raise ValueError("Target allocation is required for target_allocation report type")
            return TargetAllocationReport(portfolios, target_allocation)
        else:
            raise ValueError(f"Unsupported report type: {report_type}")
