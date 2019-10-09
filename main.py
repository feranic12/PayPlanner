from PyQt5 import QtWidgets
import application, sys


# главная точка входа в приложение
def main():
    app = QtWidgets.QApplication(sys.argv)
    my_main_window = application.MyApp()
    #my_main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()