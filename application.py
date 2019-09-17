from plyer import notification
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout,QHBoxLayout, QWidget, QTableWidget,QTableWidgetItem, QPushButton
from PyQt5.QtCore import QSize, Qt
import sys


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(895, 400))
        self.setWindowTitle("Подписчик")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vbox = QVBoxLayout()
        central_widget.setLayout(vbox)
        table = QTableWidget(self)
        table.setColumnCount(7)
        table.setRowCount(10)
        headers=["Название сервиса", "Состояние подписки", "Банк карты", "Номер карты", "Срок окончания",
                 "Период продления", "Сумма"]
        table.setHorizontalHeaderLabels(headers)
        for x in range(table.columnCount()-1):
            table.horizontalHeaderItem(x).setTextAlignment(Qt.AlignCenter)
            table.setColumnWidth(x,125)
        button1 = QPushButton()
        button1.setText("Сохранить")
        button2 = QPushButton()
        button2.setText("Уведомление")
        # button1.clicked.connect()
        button2.clicked.connect(self.send_notification)

        vbox.addWidget(table)
        hbox = QHBoxLayout()
        hbox.addWidget(button1)
        hbox.addWidget(button2)
        vbox.addLayout(hbox)

    def send_notification(self):
        notification.notify(
            title = 'Мое уведомление',
            message = 'Система уведомляет Вас о бренности бытия.',
            app_name = 'PayPlanner',
            app_icon = 'icons/icon1.ico'
        )



