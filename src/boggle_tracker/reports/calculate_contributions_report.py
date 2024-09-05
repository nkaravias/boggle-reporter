from typing import Dict
from boggle_tracker.reports.base_report import BaseReport


class CalculateContributionsReport(BaseReport):
    def __init__(self, target_allocation: Dict[str, Dict[str, float]], investment_amount: float):
        self.target_allocation = target_allocation
        self.investment_amount = investment_amount

    def generate_data(self):
        contributions = {}
        for item in self.target_allocation['target_asset_allocation']:
            symbol = item['symbol']
            percentage = item['percentage']
            amount = self.investment_amount * (percentage / 100)
            contributions[symbol] = {
                'description': item['description'],
                'percentage': percentage,
                'amount': amount
            }

        return {
            'investment_amount': self.investment_amount,
            'contributions': contributions
        }

    def get_report_type(self):
        return "calculate_contributions"
