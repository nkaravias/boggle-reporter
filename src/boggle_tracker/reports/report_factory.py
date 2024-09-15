from typing import List
from boggle_tracker.reports.base_report import BaseReport
from boggle_tracker.reports.generic_overview_report import GenericOverviewReport
from boggle_tracker.reports.target_allocation_report import TargetAllocationReport
from boggle_tracker.reports.total_target_allocation_report import TotalTargetAllocationReport
from boggle_tracker.reports.calculate_contributions_report import CalculateContributionsReport
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
        elif report_type == "calculate_contributions":
            target_allocation = kwargs.get('target_allocation')
            investment_amount = kwargs.get('investment_amount')
            if not target_allocation or investment_amount is None:
                raise ValueError("Target allocation and investment amount are required for calculate_contributions report type")
            return CalculateContributionsReport(target_allocation, investment_amount)
        else:
            raise ValueError(f"Unsupported report type: {report_type}")
