from typing import List, Dict
from collections import defaultdict
from boggle_tracker.reports.base_report import BaseReport
from boggle_tracker.models.portfolio import Portfolio


class TotalTargetAllocationReport(BaseReport):
    def __init__(self, portfolios: List[Portfolio], target_allocation: Dict[str, Dict[str, float]], exchange_rates: Dict[str, float]):
        self.portfolios = portfolios
        self.target_allocation = {item['symbol']: item for item in target_allocation['target_asset_allocation']}
        self.exchange_rates = exchange_rates
        self.base_currency = 'CAD'  # Assuming CAD as the base currency for target assets

    def generate_data(self):
        total_holdings, total_value_cad, detailed_holdings, portfolio_totals = self._aggregate_holdings()

        report_data = {
            'total_value': total_value_cad,
            'holdings': {},
            'base_currency': self.base_currency,
            'other_holdings': total_holdings.get('OTHER', 0),
            'detailed_holdings': detailed_holdings,
            'portfolio_totals': portfolio_totals
        }

        for symbol, target_info in self.target_allocation.items():
            current_value = total_holdings.get(symbol, 0)
            current_percentage = (current_value / total_value_cad) * 100 if total_value_cad else 0
            target_percentage = target_info['percentage']
            difference = current_percentage - target_percentage
            target_value = total_value_cad * (target_percentage / 100)
            action_value = target_value - current_value

            report_data['holdings'][symbol] = {
                'description': target_info['description'],
                'current_value': current_value,
                'current_percentage': current_percentage,
                'target_percentage': target_percentage,
                'difference': difference,
                'action': 'BUY' if action_value > 0 else 'SELL' if action_value < 0 else 'HOLD',
                'action_value': abs(action_value)
            }

        return report_data

    def get_report_type(self):
        return "total_target_allocation"

    def _aggregate_holdings(self):
        total_holdings = defaultdict(float)
        total_value_cad = 0
        detailed_holdings = defaultdict(list)
        portfolio_totals = {}

        for portfolio in self.portfolios:
            portfolio_total = 0
            for holding in portfolio.holdings:
                symbol = holding.get("Symbol", "N/A")
                current_price = self._safe_float(holding.get("Current Price"))
                quantity = self._safe_float(holding.get("Quantity"))
                if current_price is not None and quantity is not None:
                    market_value = current_price * quantity
                    market_value_cad = self._convert_to_cad(market_value, portfolio.currency)
                    total_value_cad += market_value_cad
                    portfolio_total += market_value_cad
                    if symbol in self.target_allocation:
                        total_holdings[symbol] += market_value_cad
                        detailed_holdings[symbol].append({
                            'portfolio_name': portfolio.name,
                            'market_value': market_value_cad,
                            'portfolio_percentage': 0  # We'll calculate this after we have the portfolio total
                        })
                    else:
                        total_holdings['OTHER'] += market_value_cad

            portfolio_totals[portfolio.name] = portfolio_total

            # Calculate portfolio percentages
            for symbol, holdings in detailed_holdings.items():
                for holding in holdings:
                    if holding['portfolio_name'] == portfolio.name:
                        holding['portfolio_percentage'] = (holding['market_value'] / portfolio_total) * 100

        return total_holdings, total_value_cad, detailed_holdings, portfolio_totals

    def _convert_to_cad(self, value, from_currency):
        if from_currency == self.base_currency:
            return value
        return value * self.exchange_rates.get(from_currency, 1)

    @staticmethod
    def _safe_float(value):
        try:
            return float(value) if value else None
        except ValueError:
            return None
