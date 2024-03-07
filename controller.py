import wallet

# CREATE A GUI FOR CONTROLLING YOUR WALLET
# show wallet contents
# option to put other stock in stocklist / remove from stocklist
# alter cash percentage


import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("pystoxx")
        self.setFixedSize(QSize(400, 300))
        button = QPushButton("Press Me!")

        # Set the central widget of the Window.
        self.setCentralWidget(button)


def run_window(wallet):

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()