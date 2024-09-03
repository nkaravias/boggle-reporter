from typing import List, Dict


class Portfolio:
    def __init__(self, name: str, holdings: List[Dict], currency: str):
        self.name = name
        self.holdings = holdings
        self.currency = currency.upper()
