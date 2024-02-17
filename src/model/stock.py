from .stock_symbols_enum import StockSymbolsEnum


class Stock(object):
    def __init__(self,
                 symbol: StockSymbolsEnum):
        self.symbol: StockSymbolsEnum = symbol
        self.avg_price: float = 0
        self.qty: float = 0
    
    def sell_units(self,
                   units: float,
                   price: float):
        assert units <= self.qty, "Cannot sell more stocks than possessed"
        if self.qty == units:
            self.avg_price = 0
            self.qty = 0
            return
        # TODO: fix this logic
        self.avg_price = ((self.qty * self.avg_price) - (units * price)) / (self.qty - units)
        self.qty -= units
    
    def to_json(self):
        return {
            "symbol":    self.symbol.value,
            "avg_price": self.avg_price,
            "qty":       self.qty
        }
