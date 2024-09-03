from collections import defaultdict
from boggle_tracker.reports.base_report import BaseReport


class GenericPortfolioOverviewReport(BaseReport):
    def generate(self):
        report_content = "Generic Portfolio Overview Report\n\n"
        currency_summaries = defaultdict(lambda: {"market_value": 0, "cost_basis": 0})

        for portfolio in self.portfolios:
            report_content += self._generate_portfolio_report(portfolio, currency_summaries)

        report_content += self._generate_currency_summaries(currency_summaries)

        self.output.output(report_content)

    def _generate_portfolio_report(self, portfolio, currency_summaries):
        report_content = f"Portfolio: {portfolio.name} ({portfolio.currency})\n"
        report_content += "Symbol\tMarket Value\tCost Basis\tUnrealized Gain/Loss\n"

        total_market_value = 0
        total_cost_basis = 0

        for holding in portfolio.holdings:
            try:
                symbol = holding.get('Symbol', 'N/A')
                current_price = self.safe_float(holding.get('Current Price'))
                quantity = self.safe_float(holding.get('Quantity'))
                purchase_price = self.safe_float(holding.get('Purchase Price'))

                if current_price is None or quantity is None:
                    print(
                        f"Missing data for holding {symbol}. Skipping holding."
                    )
                    continue

                market_value = current_price * quantity
                cost_basis = (
                    purchase_price * quantity if purchase_price is not None else 0
                )
                unrealized_gain_loss = market_value - cost_basis

                report_content += f"{symbol}\t${market_value:.2f}\t${cost_basis:.2f}\t${unrealized_gain_loss:.2f}\n"

                total_market_value += market_value
                total_cost_basis += cost_basis
            except Exception as e:
                print(f"Warning: Error processing holding: {e}. Skipping this holding.")

        total_unrealized_gain_loss = total_market_value - total_cost_basis
        report_content += f"\nTotal Market Value: ${total_market_value:.2f}\n"
        report_content += f"Total Cost Basis: ${total_cost_basis:.2f}\n"
        report_content += f"Total Unrealized Gain/Loss: ${total_unrealized_gain_loss:.2f}\n\n"

        currency_summaries[portfolio.currency]["market_value"] += total_market_value
        currency_summaries[portfolio.currency]["cost_basis"] += total_cost_basis

        return report_content

    def _generate_currency_summaries(self, currency_summaries):
        report_content = "Currency Summaries\n\n"
        for currency, summary in currency_summaries.items():
            market_value = summary["market_value"]
            cost_basis = summary["cost_basis"]
            unrealized_gain_loss = market_value - cost_basis
            report_content += f"Currency: {currency}\n"
            report_content += f"Total Market Value: ${market_value:.2f}\n"
            report_content += f"Total Cost Basis: ${cost_basis:.2f}\n"
            report_content += f"Total Unrealized Gain/Loss: ${unrealized_gain_loss:.2f}\n\n"
        return report_content

    def safe_float(self, value):
        try:
            return float(value) if value else None
        except ValueError:
            return None
