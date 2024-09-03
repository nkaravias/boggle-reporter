from typing import List
from boggle_tracker.reports.base_report import BaseReport
from boggle_tracker.reports.generic_overview_report import GenericOverviewReport
from boggle_tracker.reports.target_allocation_report import TargetAllocationReport
from boggle_tracker.reports.total_target_allocation_report import TotalTargetAllocationReport
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
        elif report_type == "total_target_allocation":
            target_allocation = kwargs.get('target_allocation')
            exchange_rates = kwargs.get('exchange_rates')
            if not target_allocation or not exchange_rates:
                raise ValueError("Target allocation and exchange rates are required for total_target_allocation report type")
            return TotalTargetAllocationReport(portfolios, target_allocation, exchange_rates)
        else:
            raise ValueError(f"Unsupported report type: {report_type}")
