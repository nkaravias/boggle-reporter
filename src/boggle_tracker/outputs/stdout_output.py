from boggle_tracker.outputs.base_output import BaseOutput


class StdoutOutput(BaseOutput):
    def output(self, data: dict, report_type: str):
        if report_type == "generic_overview":
            self._output_generic_overview(data)
        elif report_type == "target_allocation":
            self._output_target_allocation(data)
        else:
            raise ValueError(f"Unsupported report type: {report_type}")

    def _output_generic_overview(self, data):
        for portfolio_name, portfolio_data in data.items():
            print(f"Portfolio: {portfolio_name}")
            print(f"Currency: {portfolio_data['currency']}")
            print(f"Total Market Value: ${portfolio_data['total_value']:.2f}")
            print(
                "\nSymbol    Quantity    Current Price    Market Value    Purchase Price    Cost Basis"
            )
            print("-" * 80)
            for holding in portfolio_data["holdings"]:
                if holding["symbol"] == "$$CASH":
                    print(
                        f"{'$$CASH':<10} {holding['quantity']:<11.2f} {'N/A':<15} ${holding['market_value']:<15.2f} {'N/A':<17} ${holding['cost_basis']:.2f}"
                    )
                else:
                    print(
                        f"{holding['symbol']:<10} {holding['quantity']:<11.2f} ${holding['current_price']:<15.2f} ${holding['market_value']:<15.2f} ${holding['purchase_price']:<17.2f} ${holding['cost_basis']:.2f}"
                    )
            print("\n")

    def _output_target_allocation(self, data):
        for currency, report_data in data.items():
            print(f"Currency: {currency}")
            print(f"Total Market Value: ${report_data['total_value']:.2f}\n")
            print(
                f"{'Symbol':<10} {'Market Value':<15} {'Current Allocation':<20} {'Target Allocation':<20} {'Difference':<15}"
            )
            print("-" * 80)
            for symbol, value in report_data["holdings"].items():
                current_percentage = (value / report_data["total_value"]) * 100
                target_percentage = report_data["target_allocation"].get(symbol, 0)
                difference = current_percentage - target_percentage
                print(
                    f"{symbol:<10} ${value:<14.2f} {current_percentage:18.2f}% {target_percentage:18.2f}% {difference:+14.2f}%"
                )
            print("\n")
