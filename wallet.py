from actions import Conversion, get_stock_value

class Wallet:
    def __init__(self, name, amt_start, stocks):
        self.name = name
        self.amt_start = Conversion.euro_to_dollar(self,amt_start)
        self.amt_cash = self.amt_start
        self.stocks = stocks #nested dictionaries
        self.stocks_value = 0.0
        self.amt_current = self.amt_cash + self.stocks_value

    def __str__(self):
        stocksymbols=[]
        for x in self.stocks.values():
            stocksymbols.append(x['handler'].symbol)
        return f"{self.name.upper()}: \ncurrent amt: {self.amt_current}  start amt: {self.amt_start}  stocks: {stocksymbols} \n"

    def stock_add(self, stock):
        self.stocks.append(stock)

    def stock_remove(self, stockname):
        #subtract from amount of shares and remove from list if none are left
        pass


    def calculate_stocks_value(self):
        # get current value of stocks in wallet and * amount
        total_worth = 0.0
        stocks = self.stocks.values()
        for stock in stocks:
            stock_handler = stock['handler']
            total_worth += get_stock_value(stock_handler) * stock['amount']
        self.stocks_value = total_worth
        self.update_amt_current()
        return total_worth

    def update_amt_current(self):
        self.amt_current = self.amt_cash + self.stocks_value
