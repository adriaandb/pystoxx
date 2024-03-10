import wallet

# CREATE A GUI FOR CONTROLLING YOUR WALLET
# show wallet contents
# option to put other stock in stocklist / remove from stocklist
# alter cash percentage


import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

global wallet_current
# wallet_current = wallet.Wallet('dummy', 0  ,None)


def run_gui(wallet):
    global wallet_current
    wallet_current = wallet
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
        button = QPushButton(str(wallet_current.amt_current))
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        # Set the central widget of the Window.
        self.setCentralWidget(button)


    def the_button_was_clicked(self):
        print("the_button_was_clicked")







