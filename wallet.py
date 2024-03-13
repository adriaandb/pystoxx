from actions import Conversion, get_stock_value, log

class Wallet:
    def __init__(self, name, amt_start, stocks):
        self.name = name
        self.amt_start = Conversion.euro_to_dollar(self,amt_start)     # does this work?
        self.amt_cash = self.amt_start
        self.stocks = stocks #nested dictionaries
        self.stocks_value = 0.0
        self.amt_current = self.amt_cash + self.stocks_value
        self.trade_percentage = 0.0

    def __str__(self):
        stocksymbols=[]
        for x in self.stocks.values():
            stocksymbols.append(x['handler'].symbol)
        return f"{self.name.upper()}: \ncurrent amt: {self.amt_current}  \nstart amt: {self.amt_start}  \nstocks: {stocksymbols} \n"

    def stock_add(self, stock):
        self.stocks.append(stock)     # does this work on a dictionary?

    def stock_remove(self, stockname):
        #subtract from amount of shares and remove from list if none are left
        pass


    def update_stocks_value(self):
        # get current value of stocks in wallet and * amount
        total_worth_stocks = 0.0
        stocks = self.stocks.values()
        for stock in stocks:
            stock_handler = stock['handler']
            total_worth_stocks += get_stock_value(stock_handler) * stock['amount']
        self.stocks_value = total_worth_stocks
        self.update_amt_current()
        return self.stocks_value

    def update_amt_current(self):
        self.amt_current = self.amt_cash + self.stocks_value
        return self.amt_current

    def update_trade_percentage(self, tp):
        if 0 <= tp <= 100:
            try:
                self.trade_percentage = tp
                print(f'--------------------------------------------TRADE PERCENTAGE CHANGED TO {self.trade_percentage}')
                log('TRADE PERCENTAGE ADJUSTED TO ' + str(self.trade_percentage)+'\n')
            except:
                print('TP UPDATE FAILED')

    # amount of cash left over to be spent
    def get_cash_permitted_netto(self):
        cash_permitted = self.amt_current * (self.trade_percentage / 100) - self.stocks_value
        if cash_permitted > 0:
            return cash_permitted
        else:
            return 0

    # total amount of cash allowed to be spent
    def get_cash_permitted_bruto(self):
        cash_permitted = self.amt_current * (self.trade_percentage / 100)
        return cash_permitted