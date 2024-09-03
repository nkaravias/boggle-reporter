from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from boggle_tracker.outputs.base_output import BaseOutput


class RichOutput(BaseOutput):
    def __init__(self):
        self.console = Console()

    def output(self, data: dict, report_type: str):
        if report_type == "generic_overview":
            self._output_generic_overview(data)
        elif report_type == "target_allocation":
            self._output_target_allocation(data)
        else:
            raise ValueError(f"Unsupported report type: {report_type}")

    def _output_generic_overview(self, data):
        for portfolio_name, portfolio_data in data.items():
            self._format_generic_overview(portfolio_name, portfolio_data)

    def _output_target_allocation(self, data):
        for currency, report_data in data.items():
            self._format_target_allocation_report(currency, report_data)

    def _format_generic_overview(self, portfolio_name, portfolio_data):
        table = Table(title=f"Portfolio Overview: {portfolio_name}")
        table.add_column("Symbol", style="cyan", no_wrap=True)
        table.add_column("Quantity", style="magenta")
        table.add_column("Current Price", style="green")
        table.add_column("Market Value", style="yellow")
        table.add_column("Purchase Price", style="blue")
        table.add_column("Cost Basis", style="red")

        for holding in portfolio_data['holdings']:
            table.add_row(
                holding['symbol'],
                f"{holding['quantity']:.2f}",
                f"${holding['current_price']:.2f}",
                f"${holding['market_value']:.2f}",
                f"${holding['purchase_price']:.2f}",
                f"${holding['cost_basis']:.2f}"
            )

        summary = Text.assemble(
            ("Portfolio: ", "bold"),
            (portfolio_name, "cyan"),
            "\n",
            ("Currency: ", "bold"),
            (portfolio_data['currency'], "green"),
            "\n",
            ("Total Market Value: ", "bold"),
            (f"${portfolio_data['total_value']:.2f}", "yellow")
        )

        self.console.print(Panel(summary))
        self.console.print(table)
        self.console.print("\n")

    def _format_target_allocation_report(self, currency, report_data):
        table = Table(title=f"Target Asset Allocation Report - {currency}")
        table.add_column("Symbol", style="cyan", no_wrap=True)
        table.add_column("Market Value", style="magenta")
        table.add_column("Current Allocation", style="green")
        table.add_column("Target %", style="yellow")
        table.add_column("Target Allocation", style="blue")
        table.add_column("Difference", style="red")
        table.add_column("Action", style="bold")
        table.add_column("Amount", style="magenta")

        total_value = report_data['total_value']
        holdings = report_data['holdings']
        target_allocation = report_data['target_allocation']

        for symbol, value in holdings.items():
            current_percentage = (value / total_value) * 100
            target_percentage = target_allocation.get(symbol, 0)
            difference = current_percentage - target_percentage
            target_value = total_value * (target_percentage / 100)
            amount_difference = target_value - value

            action = "HOLD"
            if amount_difference > 0:
                action = "BUY"
            elif amount_difference < 0:
                action = "SELL"

            table.add_row(
                symbol,
                f"${value:.2f}",
                f"{current_percentage:.2f}%",
                f"{target_percentage:.2f}%",
                f"${target_value:.2f}",
                f"{difference:+.2f}%",
                action,
                f"${abs(amount_difference):.2f}"
            )

        # Add summary row
        table.add_row(
            "ALL",
            f"${total_value:.2f}",
            "100.00%",
            "100.00%",
            f"${total_value:.2f}",
            "0.00%",
            "N/A",
            "N/A",
            style="bold"
        )

        summary = Text(f"\nTotal Market Value: ${total_value:.2f}", style="bold green")
        self.console.print(Panel(summary))
        self.console.print(table)
        self.console.print("\n")
