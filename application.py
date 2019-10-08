from plyer import notification
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout,QHBoxLayout, QWidget, QTableWidget,QTableWidgetItem, QPushButton, QMessageBox
from PyQt5.QtCore import QSize, Qt, QDate
from PyQt5 import QtGui
import sys, db
from datetime import date, timedelta
from time import strptime, mktime, sleep
from add_form import AddForm
from edit_form import EditForm


# класс приложения, представляющий главное окно приложения
class MyApp(QMainWindow):
    # инициализация элементов главного окна
    def __init__(self):
        super().__init__()
        self.db_driver = db.DB()
        self.subscriptions = self.db_driver.get_all_subscriptions()
        self.setMinimumSize(QSize(1360, 450))
        self.setWindowTitle("Подписчик")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        vbox = QVBoxLayout()
        self.central_widget.setLayout(vbox)
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        headers = ["Название сервиса", "Состояние подписки", "Банк карты", "Платежная система", "Номер карты",
                   "Период продления","Сумма", "Срок окончания"]
        self.table.setRowCount(self.db_driver.get_subs_count())
        self.table.setHorizontalHeaderLabels(headers)
        for x in range(self.table.columnCount()):
            self.table.horizontalHeaderItem(x).setTextAlignment(Qt.AlignCenter)
            self.table.horizontalHeaderItem(x).setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
            self.table.setColumnWidth(x,160)
            cellinfo = QTableWidgetItem(headers[x])
            cellinfo.setTextAlignment(Qt.AlignCenter)

        self.button1 = QPushButton()
        self.button1.setText("Добавить")
        self.button2 = QPushButton()
        self.button2.setText("Редактировать")
        self.button3 = QPushButton()
        self.button3.setText("Удалить")
        self.button4 = QPushButton()
        self.button4.setText("Проверить")

        self.button1.clicked.connect(self.add_new_subscription)
        self.button2.clicked.connect(self.edit_selected)
        self.button3.clicked.connect(self.delete_subscription)
        self.button4.clicked.connect(self.check_updates)
        self.table.doubleClicked.connect(self.edit_selected)

        vbox.addWidget(self.table)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)
        hbox.addWidget(self.button3)
        hbox.addWidget(self.button4)
        vbox.addLayout(hbox)
        sleep(10)
        self.check_updates()
        self.load_from_file()
        self.set_readonly()

    # установка запрета на редактирование ячеек таблицы
    def set_readonly(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                cellinfo = QTableWidgetItem(self.table.item(row,col))
                cellinfo.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row, col, cellinfo)

    # проверка необходимости продления каких-либо подписок
    def check_updates(self):
        self.subscriptions = self.db_driver.get_all_subscriptions()
        # n - число подписок, оканчивающихся сегодня
        n = 0
        for sub in self.subscriptions:
            sub_list = list(sub)
            end_date = date.fromtimestamp(mktime(strptime(sub_list[6], "%Y-%m-%d")))
            # увеличение даты окончания периода подписки на месяц/год
            new_end_date = None
            if end_date == date.today():
                n = n + 1
                # ежемесячная подписка
                if sub_list[4] == 0:
                    if end_date.month == 12:
                        new_end_date = date(end_date.year + 1, 1, end_date.day)
                    else:
                        new_end_date = date(end_date.year, end_date.month + 1, end_date.day)
                # ежегодная подписка
                elif sub_list[4] == 1:
                    new_end_date = date(end_date.year + 1, end_date.month, end_date.day)
                self.db_driver.update_end_date(sub[0], new_end_date)

            # Отправка уведомления о продлении подписки
            if end_date <= date.today()+timedelta(1):
                sleep(5)
                self.send_notification(sub)

        # если были подписки, оканчивающиеся сегодня, перезагрузить таблицу
        if n > 0:
            self.load_from_file()
            return True
        else:
            return False

    # отправка push уведомления в трей Windows о том, что скоро оканчивается срок подписки
    def send_notification(self, sub):
        for bc in self.db_driver.get_all_bank_cards():
            if bc[0] == sub[3]:
                card_str = bc[3] + ' ' + bc[1][-4:]
        notification.notify(
            title='ПОДПИСЧИК',
            message=sub[6] + ' истекает срок продления подписки ' + sub[1] + ' . Будет списано ' + str(sub[5]) + ' рублей со счета ' + card_str,
            app_name='PayPlanner',
            app_icon='icons/icon1.ico'
        )

    # заполнение таблицы актуальными данными из БД
    def load_from_file(self):
        self.table.clearContents()
        subs_for_table = self.db_driver.get_subs_for_table()
        for row in range(subs_for_table.__len__()):
            for col in range(self.table.columnCount()):
                cellinfo = QTableWidgetItem(str(subs_for_table[row][col]))
                self.table.setItem(row, col, cellinfo)

    # вызов формы добавления записи в таблицу
    def add_new_subscription(self):
        self.add_form = AddForm(self)
        self.add_form.show()

    # вызов формы редактирования записи табицы
    def edit_selected(self):
        row_num = self.table.currentRow()
        sub = self.db_driver.get_all_subscriptions()[row_num]
        self.edit_form = EditForm(self, sub)
        self.edit_form.show()

    # удаление выбранной записи из таблицы
    def delete_subscription(self):
        row_num = self.table.currentRow()
        id = self.db_driver.get_all_subscriptions()[row_num][0]
        self.db_driver.delete_sub(id)
        self.table.setRowCount(self.table.rowCount() - 1)
        self.load_from_file()




