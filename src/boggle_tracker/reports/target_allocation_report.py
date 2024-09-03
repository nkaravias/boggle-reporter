from typing import List, Dict
from collections import defaultdict
from boggle_tracker.reports.base_report import BaseReport
from boggle_tracker.models.portfolio import Portfolio


class TargetAllocationReport(BaseReport):
    def __init__(self, portfolios: List[Portfolio], target_allocation: Dict[str, float]):
        self.portfolios = portfolios
        self.target_allocation = target_allocation

    def generate_data(self):
        currency_holdings = self._aggregate_holdings_by_currency()
        report_data = {}

        for currency, holdings in currency_holdings.items():
            total_value = sum(holdings.values())
            report_data[currency] = {
                'holdings': holdings,
                'total_value': total_value,
                'target_allocation': self.target_allocation
            }

        return report_data

    def get_report_type(self):
        return "target_allocation"

    def _aggregate_holdings_by_currency(self):
        currency_holdings = defaultdict(lambda: defaultdict(float))
        for portfolio in self.portfolios:
            for holding in portfolio.holdings:
                symbol = holding.get("Symbol", "N/A")
                current_price = self._safe_float(holding.get("Current Price"))
                quantity = self._safe_float(holding.get("Quantity"))

                if current_price is not None and quantity is not None:
                    market_value = current_price * quantity
                    currency_holdings[portfolio.currency][symbol] += market_value

        return currency_holdings

    @staticmethod
    def _safe_float(value):
        try:
            return float(value) if value else None
        except ValueError:
            return None
