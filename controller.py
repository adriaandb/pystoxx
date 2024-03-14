import wallet

# CREATE A GUI FOR CONTROLLING YOUR WALLET
# show wallet contents
# option to put other stock in stocklist / remove from stocklist
# alter trade percentage


import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit

global wallet_current
# wallet_current = wallet.Wallet('dummy', 0  ,None)

# to print out silent exceptions
sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook


def run_gui(wallet):
    global wallet_current
    wallet_current = wallet
    gui = QApplication.instance()
    if gui is None:
        gui = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    gui.exec()


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("pystoxx")
        self.setFixedSize(QSize(400, 300))


        wallet_info = QLabel(str(wallet_current))
        wallet_amt_cash = QLabel("amount of cash:  " + str(wallet_current.amt_cash))
        wallet_current.update_stocks_value()
        wallet_profit = QLabel(f'profit: {wallet_current.amt_current - wallet_current.amt_start}')

        label_tp = QLabel(f'{round(wallet_current.get_cash_permitted_netto(), 2)} left for trading with trade percentage {wallet_current.trade_percentage}%')
        label_amt = QLabel(f'{round(wallet_current.stocks_value, 2)} of {round(wallet_current.get_cash_permitted_bruto(), 2)} converted to stock.\n')

        self.input_bar = QLineEdit()
        self.input_bar.setPlaceholderText("enter new trade percentage (press enter)")
        self.input_bar .returnPressed.connect(self.input_bar_return_pressed)

        button = QPushButton('click to refresh')
        button.setCheckable(False)
        button.clicked.connect(self.load_info)

        layout = QVBoxLayout()
        layout.addWidget(wallet_info)
        layout.addWidget(wallet_amt_cash)
        layout.addWidget(wallet_profit)
        layout.addWidget((label_tp))
        layout.addWidget((label_amt))
        layout.addWidget(self.input_bar )
        layout.addWidget(button)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)

    def the_button_was_clicked(self):
        print("the_button_was_clicked")

    def load_info(self):
        wallet_info = QLabel(str(wallet_current))
        wallet_amt_cash = QLabel("amount of cash:  " + str(wallet_current.amt_cash))
        wallet_current.update_stocks_value()
        wallet_profit = QLabel(f'profit: {wallet_current.amt_current - wallet_current.amt_start}')

        label_tp = QLabel(f'{round(wallet_current.get_cash_permitted_netto(), 2)} left for trading with trade percentage {wallet_current.trade_percentage}%')
        label_amt = QLabel(f'{round(wallet_current.stocks_value, 2)} of {round(wallet_current.get_cash_permitted_bruto(), 2)} converted to stock.\n')

        self.input_bar = QLineEdit()
        self.input_bar.setPlaceholderText("enter new trade percentage (press enter)")
        self.input_bar.returnPressed.connect(self.input_bar_return_pressed)

        button = QPushButton('click to refresh')
        button.setCheckable(False)
        button.clicked.connect(self.load_info)

        layout = QVBoxLayout()
        layout.addWidget(wallet_info)
        layout.addWidget(wallet_amt_cash)
        layout.addWidget(wallet_profit)
        layout.addWidget((label_tp))
        layout.addWidget((label_amt))
        layout.addWidget(self.input_bar)
        layout.addWidget(button)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
    def input_bar_return_pressed(self):
        global line_input

        # try:
        line_input = int(self.input_bar .text())
        # except:
        #     print('please enter a number')
        #     line_input=0

        if 0 <= line_input <= 100:
            wallet_current.update_trade_percentage(line_input)
            # print(f'trade percentage: {wallet_current.trade_percentage}')
            self.load_info()
        else:
            line_input=0
            print('please enter a number between 0-100')


    def line_text_edited(self, s):
        print(f'linetext: {s}\n')




