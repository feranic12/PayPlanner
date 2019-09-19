from plyer import notification
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout,QHBoxLayout, QWidget, QTableWidget,QTableWidgetItem, QPushButton
from PyQt5.QtCore import QSize, Qt
import sys, db
from datetime import date, timedelta


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
                    cellinfo = QTableWidgetItem("")
                    cellinfo.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.table.setItem(row, col, cellinfo)

        self.button1 = QPushButton()
        self.button1.setText("Добавить")
        self.button2 = QPushButton()
        self.button2.setText("Редактировать")
        self.button3 = QPushButton()
        self.button3.setText("Удалить")
        self.button4 = QPushButton()
        self.button4.setText("Уведомление")
        self.button4.clicked.connect(self.send_notification)

        vbox.addWidget(self.table)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)
        hbox.addWidget(self.button3)
        hbox.addWidget(self.button4)
        vbox.addLayout(hbox)

        self.load_from_file()

    def send_notification(self):
        notification.notify(
            title = 'Мое уведомление',
            message = 'Система уведомляет Вас о бренности бытия.',
            app_name = 'PayPlanner',
            app_icon = 'icons/icon1.ico'
        )

    def load_from_file(self):
        db_driver = db.DB()
        row1 = db_driver.get_all_rows()
        for col in range(self.table.columnCount()):
            cellinfo = QTableWidgetItem(str(row1[col]))
            self.table.setItem(0, col, cellinfo)
        db_driver.quit()


