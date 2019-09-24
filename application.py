from plyer import notification
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout,QHBoxLayout, QWidget, QTableWidget,QTableWidgetItem, QPushButton
from PyQt5.QtCore import QSize, Qt, QDate
import sys, db
from datetime import date, timedelta
from add_form import AddForm
from edit_form import EditForm


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_driver = db.DB()
        self.setMinimumSize(QSize(1325, 450))
        self.setWindowTitle("Подписчик")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        vbox = QVBoxLayout()
        self.central_widget.setLayout(vbox)
        self.table = QTableWidget(self)
        self.table.setColumnCount(8)
        self.table.setRowCount(self.db_driver.get_subs_count())
        headers = ["Название сервиса", "Состояние подписки", "Банк карты", "Платежная система", "Номер карты",
                   "Период продления","Сумма","Срок окончания"]
        self.table.setHorizontalHeaderLabels(headers)
        for x in range(self.table.columnCount()):
            self.table.horizontalHeaderItem(x).setTextAlignment(Qt.AlignCenter)
            self.table.setColumnWidth(x,160)

        self.button1 = QPushButton()
        self.button1.setText("Добавить")
        self.button2 = QPushButton()
        self.button2.setText("Редактировать")
        self.button3 = QPushButton()
        self.button3.setText("Удалить")
        self.button4 = QPushButton()
        self.button4.setText("Уведомление")

        self.add_form = AddForm(self)
        self.edit_form = EditForm(self)

        self.button1.clicked.connect(self.add_new_subscription)
        self.button2.clicked.connect(self.edit_selected)
        self.button4.clicked.connect(self.send_notification)
        self.table.doubleClicked.connect(self.edit_selected)

        vbox.addWidget(self.table)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)
        hbox.addWidget(self.button3)
        hbox.addWidget(self.button4)
        vbox.addLayout(hbox)

        self.load_from_file()
        self.set_readonly()

    def set_readonly(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                cellinfo = QTableWidgetItem(self.table.item(row,col))
                cellinfo.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row, col, cellinfo)

    def send_notification(self):
        notification.notify(
            title = 'Мое уведомление',
            message = 'Система уведомляет Вас о бренности бытия.',
            app_name = 'PayPlanner',
            app_icon = 'icons/icon1.ico'
        )

    def load_from_file(self):
        all_rows = self.db_driver.get_all_subscriptions()
        for row in range(all_rows.__len__()):
            for col in range(self.table.columnCount()):
                cellinfo = QTableWidgetItem(str(all_rows[row][col]))
                self.table.setItem(row, col, cellinfo)

    def add_new_subscription(self):
        self.add_form.show()

    def edit_selected(self):
        row_num = self.table.currentRow()
        edit_tuple = self.db_driver.get_current_sub(row_num)
        self.edit_form.textEdit.setText(edit_tuple[1])
        self.edit_form.comboBox_3.setCurrentIndex(edit_tuple[2])
        self.edit_form.comboBox.setCurrentIndex(edit_tuple[3])
        self.edit_form.comboBox_2.setCurrentIndex(edit_tuple[4])
        self.edit_form.textEdit_2.setText(str(edit_tuple[5]))
        self.edit_form.dateEdit.setDate(QDate(int(edit_tuple[6][:4]), int(edit_tuple[6][5:7]), int(edit_tuple[6][8:10])))
        self.edit_form.show()





