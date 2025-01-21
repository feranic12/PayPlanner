
import sys

from PyQt5 import QtWidgets, QtGui

import application


# главная точка входа в приложение
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icons/icon1.ico"))
    my_main_window = application.MyApp()
    my_main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
