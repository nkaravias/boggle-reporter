# boggle-reporter
Generate reports for financial data input

A config file is required to run the program. The config file is a JSON file that contains the path to the CSV files and the currency of the portfolio.
The files are downloaded using yahoo finance's export feature. I'll try to make this more flexible in the future.

Example config file:
```json
{
    "portfolios": [
      {
        "name": "RRSP (USD)",
        "csv_path": "resources/rrsp_usd.csv",
        "currency": "USD"
      },
      {
        "name": "Self-directed (CAD)",
        "csv_path": "resources/self_directed_cad.csv",
        "currency": "CAD"
      },
      {
        "name": "Self-directed (USD)",
        "csv_path": "resources/self_directed_usd.csv",
        "currency": "USD"
      }
    ]
  }
```
## Report Types

### Generic Overview Report

This report provides a generic overview of the portfolio. It is the most basic report and is used to get a quick overview of the portfolio.
All it does is print out the total value of the portfolio and the total value of each asset class.

```bash
python src/boggle_tracker/main.py --config resources/config.json --report generic_overview
```



### Target Allocation Report

This report provides a target allocation report. It accepts a target allocation config file which is a JSON file that contains the target asset allocation.
It then calculates the current allocation of each asset and determines alignment with the target allocation.

```bash
python src/boggle_tracker/main.py --report target_allocation --target-allocation resources/target_allocation_config.json --output stdout config.json
```

Example target allocation config file:
```json
{
  "target_asset_allocation": [
    {
      "symbol": "VCN",
      "description": "Canadian Equity",
      "percentage": 25
    },
    {
      "symbol": "XUU",
      "description": "Total U.S. Market Fund",
      "percentage": 40
    },
    {
      "symbol": "XAW",
      "description": "International Equity",
      "percentage": 15
    },
    {
      "symbol": "ZAG",
      "description": "Canadian Aggregate Bonds",
      "percentage": 20
    }
  ]
}
```



## Outputs

Currently stdout and rich are supported via the --output flag.

```bash
python src/boggle_tracker/main.py --config resources/config.json --report generic_overview --output rich
```
