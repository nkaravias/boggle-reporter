# src/boggle_tracker/main.py
import argparse
import json
from boggle_tracker.config import load_config
from boggle_tracker.models.portfolio import Portfolio
from boggle_tracker.reports.report_factory import ReportFactory
from boggle_tracker.outputs.output_factory import OutputFactory
from boggle_tracker.utils.csv_loader import load_csv


def load_portfolios(config_path: str):
    config = load_config(config_path)
    portfolios = []
    for portfolio_config in config['portfolios']:
        holdings = load_csv(portfolio_config['csv_path'])
        portfolios.append(
            Portfolio(portfolio_config["name"], holdings, portfolio_config["currency"])
        )
    return portfolios


def load_target_allocation(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)


def load_exchange_rates(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Boggle Tracker - Portfolio Analysis Tool")
    parser.add_argument("config", help="Path to the data config file")
    parser.add_argument(
        "--report",
        choices=["generic_overview", "target_allocation", "total_target_allocation"],
        default="generic_overview",
        help="Type of report to generate",
    )
    parser.add_argument(
        "--output",
        choices=["stdout", "rich"],
        default="rich",
        help="Output type for the report",
    )
    parser.add_argument(
        "--target-allocation",
        help="Path to the target allocation configuration file (required for target_allocation and total_target_allocation reports)",
    )
    parser.add_argument(
        "--exchange-rates",
        help="Path to the exchange rates configuration file (required for total_target_allocation report)",
    )

    args = parser.parse_args()

    portfolios = load_portfolios(args.config)
    output = OutputFactory.create(args.output)

    report_kwargs = {}
    if args.report in ["target_allocation", "total_target_allocation"]:
        if not args.target_allocation:
            parser.error(f"--target-allocation is required for {args.report} report")
        report_kwargs['target_allocation'] = load_target_allocation(args.target_allocation)

    if args.report == "total_target_allocation":
        if not args.exchange_rates:
            parser.error("--exchange-rates is required for total_target_allocation report")
        report_kwargs['exchange_rates'] = load_exchange_rates(args.exchange_rates)

    report = ReportFactory.create(args.report, portfolios, **report_kwargs)
    data = report.generate_data()
    output.output(data, report.get_report_type())


if __name__ == "__main__":
    main()
