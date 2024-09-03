import argparse
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


def main():
    parser = argparse.ArgumentParser(description="Boggle Tracker - Portfolio Analysis Tool")
    parser.add_argument("config", help="Path to the data config file")
    parser.add_argument(
        "--report",
        choices=["generic_overview"],
        default="generic_overview",
        help="Type of report to generate",
    )
    parser.add_argument(
        "--output",
        choices=["stdout"],
        default="stdout",
        help="Output type for the report",
    )

    args = parser.parse_args()

    portfolios = load_portfolios(args.config)
    output = OutputFactory.create(args.output)
    report = ReportFactory.create(args.report, portfolios, output)
    report.generate()


if __name__ == "__main__":
    main()
