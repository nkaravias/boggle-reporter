from typing import List
# from collections import defaultdict
from boggle_tracker.reports.base_report import BaseReport
from boggle_tracker.models.portfolio import Portfolio


class GenericOverviewReport(BaseReport):
    def __init__(self, portfolios: List[Portfolio]):
        self.portfolios = portfolios

    def generate_data(self):
        report_data = {}
        for portfolio in self.portfolios:
            portfolio_data = self._process_portfolio(portfolio)
            report_data[portfolio.name] = portfolio_data
        return report_data

    def get_report_type(self):
        return "generic_overview"

    def _process_portfolio(self, portfolio):
        total_value = 0
        holdings_data = []
        cash_total = 0

        for holding in portfolio.holdings:
            symbol = holding.get('Symbol', 'N/A')

            if symbol == '$$CASH':
                cash_total += self._safe_float(holding.get('Quantity', 0))
                continue

            market_value = self._calculate_market_value(holding)
            total_value += market_value

            holding_data = {
                'symbol': symbol,
                'quantity': self._safe_float(holding.get('Quantity')),
                'current_price': self._safe_float(holding.get('Current Price')),
                'market_value': market_value,
                'purchase_price': self._safe_float(holding.get('Purchase Price')),
                'cost_basis': self._calculate_cost_basis(holding),
            }
            holdings_data.append(holding_data)

        if cash_total != 0:
            holdings_data.append({
                'symbol': '$$CASH',
                'quantity': cash_total,
                'current_price': 1,
                'market_value': cash_total,
                'purchase_price': 1,
                'cost_basis': cash_total,
            })
            total_value += cash_total

        return {
            'currency': portfolio.currency,
            'total_value': total_value,
            'holdings': holdings_data
        }

    def _calculate_market_value(self, holding):
        quantity = self._safe_float(holding.get('Quantity'))
        current_price = self._safe_float(holding.get('Current Price'))
        return quantity * current_price if quantity and current_price else 0

    def _calculate_cost_basis(self, holding):
        quantity = self._safe_float(holding.get('Quantity'))
        purchase_price = self._safe_float(holding.get('Purchase Price'))
        return quantity * purchase_price if quantity and purchase_price else 0

    @staticmethod
    def _safe_float(value):
        try:
            return float(value) if value else 0
        except ValueError:
            return 0
