from plyer import notification
from PyQt5 import QtWidgets
import MyMainWindow
import sys


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MyMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.send_notification)

    def send_notification(self):
        notification.notify(
            title = 'Мое уведомление',
            message = 'Система уведомляет Вас о бренности бытия.',
            app_name = 'PayPlanner'
        )



