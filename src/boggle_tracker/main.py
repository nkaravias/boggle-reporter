# src/boggle_tracker/main.py

import argparse
import csv
import json
from pathlib import Path
from typing import List, Dict
from collections import defaultdict


class Portfolio:
    def __init__(self, name: str, holdings: List[Dict], currency: str):
        self.name = name
        self.holdings = holdings
        self.currency = currency.upper()


class ReportOutput:
    def output(self, content: str):
        pass


class StdoutReportOutput(ReportOutput):
    def output(self, content: str):
        print(content)


class ReportOutputFactory:
    @staticmethod
    def create(output_type: str) -> ReportOutput:
        if output_type == 'stdout':
            return StdoutReportOutput()
        else:
            raise ValueError(f"Unsupported output type: {output_type}")


class Report:
    def __init__(self, portfolios: List[Portfolio], output: ReportOutput):
        self.portfolios = portfolios
        self.output = output

    def generate(self):
        pass


class GenericPortfolioOverviewReport(Report):
    def generate(self):
        report_content = "Generic Portfolio Overview Report\n\n"
        currency_summaries = defaultdict(lambda: {"market_value": 0, "cost_basis": 0})

        for portfolio in self.portfolios:
            report_content += self.generate_portfolio_report(portfolio, currency_summaries)

        report_content += self.generate_currency_summaries(currency_summaries)

        self.output.output(report_content)

    def generate_portfolio_report(self, portfolio, currency_summaries):
        report_content = f"Portfolio: {portfolio.name} ({portfolio.currency})\n"
        report_content += "Symbol\tMarket Value\tCost Basis\tUnrealized Gain/Loss\n"

        total_market_value = 0
        total_cost_basis = 0

        for holding in portfolio.holdings:
            try:
                symbol = holding['Symbol']
                current_price = self.safe_float(holding['Current Price'])
                quantity = self.safe_float(holding['Quantity'])
                purchase_price = self.safe_float(holding['Purchase Price'])

                if current_price is None or quantity is None:
                    continue  # Skip this holding if we're missing crucial data

                market_value = current_price * quantity
                cost_basis = purchase_price * quantity if purchase_price is not None else 0
                unrealized_gain_loss = market_value - cost_basis

                report_content += f"{symbol}\t${market_value:.2f}\t${cost_basis:.2f}\t${unrealized_gain_loss:.2f}\n"

                total_market_value += market_value
                total_cost_basis += cost_basis
            except KeyError as e:
                print(f"Warning: Missing key {e} in holding data. Skipping this holding.")
            except Exception as e:
                print(f"Warning: Error processing holding: {e}. Skipping this holding.")

        total_unrealized_gain_loss = total_market_value - total_cost_basis
        report_content += f"\nTotal Market Value: ${total_market_value:.2f}\n"
        report_content += f"Total Cost Basis: ${total_cost_basis:.2f}\n"
        report_content += f"Total Unrealized Gain/Loss: ${total_unrealized_gain_loss:.2f}\n\n"

        currency_summaries[portfolio.currency]["market_value"] += total_market_value
        currency_summaries[portfolio.currency]["cost_basis"] += total_cost_basis

        return report_content

    def generate_currency_summaries(self, currency_summaries):
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

    @staticmethod
    def safe_float(value):
        try:
            return float(value) if value else None
        except ValueError:
            return None


class ReportFactory:
    @staticmethod
    def create(report_type: str, portfolios: List[Portfolio], output: ReportOutput) -> Report:
        if report_type == 'generic_overview':
            return GenericPortfolioOverviewReport(portfolios, output)
        else:
            raise ValueError(f"Unsupported report type: {report_type}")


def load_portfolios(config_path: str) -> List[Portfolio]:
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    
    portfolios = []
    for portfolio_config in config['portfolios']:
        csv_path = portfolio_config['csv_path']
        try:
            with open(csv_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                holdings = list(reader)
            portfolios.append(Portfolio(portfolio_config['name'], holdings, portfolio_config['currency']))
        except FileNotFoundError:
            print(f"Warning: CSV file not found: {csv_path}. Skipping this portfolio.")
        except csv.Error as e:
            print(f"Warning: Error reading CSV file {csv_path}: {e}. Skipping this portfolio.")

    return portfolios


def main():
    parser = argparse.ArgumentParser(description="Boggle Tracker - Portfolio Analysis Tool")
    parser.add_argument("config", help="Path to the data config file")
    parser.add_argument("--report", choices=['generic_overview'], default='generic_overview', help="Type of report to generate")
    parser.add_argument("--output", choices=['stdout'], default='stdout', help="Output type for the report")

    args = parser.parse_args()

    portfolios = load_portfolios(args.config)
    output = ReportOutputFactory.create(args.output)
    report = ReportFactory.create(args.report, portfolios, output)
    report.generate()


if __name__ == "__main__":
    main()