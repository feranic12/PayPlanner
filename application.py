from plyer import notification
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout,QHBoxLayout, QWidget, QTableWidget,QTableWidgetItem, QPushButton
from PyQt5.QtCore import QSize, Qt
import sys


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(955, 400))
        self.setWindowTitle("Подписчик")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        vbox = QVBoxLayout()
        self.central_widget.setLayout(vbox)
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setRowCount(10)
        headers=["Название сервиса", "Состояние подписки", "Банк карты", "Номер карты", "Срок окончания",
                 "Период продления", "Сумма"]
        self.table.setHorizontalHeaderLabels(headers)
        for x in range(self.table.columnCount()):
            self.table.horizontalHeaderItem(x).setTextAlignment(Qt.AlignCenter)
            self.table.setColumnWidth(x,130)
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                cellinfo = QTableWidgetItem("Dookie")
                self.table.setItem(row, col, cellinfo)
        self.button1 = QPushButton()
        self.button1.setText("Редактировать")
        self.button2 = QPushButton()
        self.button2.setText("Уведомление")
        self.button1.clicked.connect(self.switch_readonly)
        self.button2.clicked.connect(self.send_notification)

        vbox.addWidget(self.table)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)
        vbox.addLayout(hbox)

    def send_notification(self):
        notification.notify(
            title = 'Мое уведомление',
            message = 'Система уведомляет Вас о бренности бытия.',
            app_name = 'PayPlanner',
            app_icon = 'icons/icon1.ico'
        )

    def switch_readonly(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                cellinfo = QTableWidgetItem("UngaBunga")
                cellinfo.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable)
                self.table.setItem(row, col, cellinfo)

