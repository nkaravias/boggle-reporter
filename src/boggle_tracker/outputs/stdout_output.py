from boggle_tracker.outputs.base_output import BaseOutput


class StdoutOutput(BaseOutput):
    def output(self, data: dict, report_type: str):
        if report_type == "generic_overview":
            self._output_generic_overview(data)
        elif report_type == "target_allocation":
            self._output_target_allocation(data)
        elif report_type == "total_target_allocation":
            self._output_total_target_allocation(data)
        elif report_type == "calculate_contributions":
            self._output_calculate_contributions(data)
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

    def _output_total_target_allocation(self, data):
        print(f"Total Target Allocation Report")
        print(f"Base Currency: {data['base_currency']}")
        print(f"Total Portfolio Value: ${data['total_value']:.2f} {data['base_currency']}\n")

        print("Overall Asset Allocation")
        print(f"{'Symbol':<10} {'Description':<25} {'Current Value':<15} {'Current %':<10} {'Target %':<10} {'Difference':<12} {'Action':<6} {'Action Value'}")
        print("-" * 100)
        for symbol, holding_data in data['holdings'].items():
            print(f"{symbol:<10} {holding_data['description']:<25} ${holding_data['current_value']:<14.2f} {holding_data['current_percentage']:9.2f}% {holding_data['target_percentage']:9.2f}% {holding_data['difference']:+11.2f}% {holding_data['action']:<6} ${holding_data['action_value']:.2f}")

        other_percentage = (data['other_holdings'] / data['total_value']) * 100
        print(f"{'OTHER':<10} {'Non-target assets':<25} ${data['other_holdings']:<14.2f} {other_percentage:9.2f}% {'N/A':9} {'N/A':11} {'N/A':<6} {'N/A'}")
        print("\n")

        print("Detailed Asset Breakdown")
        print(f"{'Symbol':<10} {'Market Value':<15} {'Portfolio Name':<25} {'Portfolio Total':<20} {'% of Portfolio'}")
        print("-" * 95)
        for symbol, holdings in data['detailed_holdings'].items():
            for holding in holdings:
                portfolio_total = data['portfolio_totals'][holding['portfolio_name']]
                print(f"{symbol:<10} ${holding['market_value']:<14.2f} {holding['portfolio_name']:<25} ${portfolio_total:<19.2f} {holding['portfolio_percentage']:9.2f}%")
        print("\n")

    def _output_calculate_contributions(self, data):
        print(f"Investment Amount: ${data['investment_amount']:.2f}\n")
        print(f"{'Symbol':<10} {'Description':<25} {'Percentage':<15} {'Amount'}")
        print("-" * 65)
        for symbol, contribution in data['contributions'].items():
            print(f"{symbol:<10} {contribution['description']:<25} {contribution['percentage']:13.2f}% ${contribution['amount']:.2f}")
        print("\n")
