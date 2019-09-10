from PyQt5 import QtWidgets
import MyMainWindow
import sys


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MyMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)


