from plyer import notification
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout,QHBoxLayout, QWidget, QTableWidget,QTableWidgetItem, QPushButton, QMessageBox
from PyQt5.QtCore import QSize, Qt, QDate
from PyQt5 import QtGui
import sys, db
from datetime import datetime, date, timedelta
from time import strptime, mktime, sleep
from add_form import AddForm
from edit_form import EditForm


# класс приложения, представляющий главное окно приложения
class MyApp(QMainWindow):
    # инициализация элементов главного окна
    def __init__(self):
        super().__init__()
        self.db_driver = db.DB()
        self.edit_form = None
        self.add_form = None
        self.t = None
        self.subscriptions = self.db_driver.get_all_subscriptions()
        self.setFixedSize(QSize(1360, 450))
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
        #sleep(10)
        self.check_updates()
        self.load_from_file()
        self.color_table()
        self.set_readonly()

    # установка запрета на редактирование ячеек таблицы
    def set_readonly(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                cellinfo = QTableWidgetItem(self.table.item(row,col))
                cellinfo.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row, col, cellinfo)

    # покраска строк таблицы
    def color_table(self):
        subs = self.subscriptions
        for row in range(self.table.rowCount()):
            state = subs[row][2]
            color = None
            if state == 0:
                color = "yellow"
            elif state == 1:
                color = "lightgreen"
            elif state == 2:
                color = "red"
            for col in range(self.table.columnCount()):
                cellinfo = QTableWidgetItem(self.table.item(row, col))
                cellinfo.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                cellinfo.setBackground(QtGui.QColor(color))
                self.table.setItem(row, col, cellinfo)

    # проверка необходимости продления каких-либо подписок
    def check_updates(self):
        self.subscriptions = self.db_driver.get_all_subscriptions()
        # n - число подписок, оканчивающихся сегодня
        n = 0
        for sub in self.subscriptions:
            sub_list = list(sub)
            end_date = datetime.strptime(sub_list[6], "%Y-%m-%d").date()
            if end_date <= date.today() + timedelta(1):
                sleep(5)
                self.send_notification(sub)
            # увеличение даты окончания периода подписки на месяц/год
            while end_date <= date.today():
                n = n + 1
                # ежемесячная подписка
                duration = self.db_driver.get_duration_by_id(sub_list[4])
                if duration + end_date.month <= 12:
                    end_date = date(end_date.year, end_date.month + duration, end_date.day)
                else:
                    end_date = date(end_date.year + 1, end_date.month + duration - 12, end_date.day)
                self.db_driver.update_end_date(sub[0], end_date)

        # если были подписки, оканчивающиеся сегодня, перезагрузить таблицу
        if n > 0:
            self.load_from_file()

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
                if col == 5:
                    cellinfo = QTableWidgetItem(str(subs_for_table[row][col]) + " мес")
                else: cellinfo = QTableWidgetItem(str(subs_for_table[row][col]))
                self.table.setItem(row, col, cellinfo)

    # вызов формы добавления записи в таблицу
    def add_new_subscription(self):
        self.add_form = AddForm(self)
        self.add_form.show()

    # вызов формы редактирования записи табицы
    def edit_selected(self):
        row_num = self.table.currentRow()
        sub = self.db_driver.get_all_subscriptions()[row_num]
        self.t = sub
        self.edit_form = EditForm(self, sub)
        self.edit_form.show()

    # удаление выбранной записи из таблицы
    def delete_subscription(self):
        row_num = self.table.currentRow()
        id = self.db_driver.get_all_subscriptions()[row_num][0]
        self.db_driver.delete_sub(id)
        self.table.setRowCount(self.table.rowCount() - 1)
        self.load_from_file()

    # сохранение новой записи в БД по кнопке "Сохранить"
    def save_new_subscription(self):
        if self.add_form.check_form():
            service_name = self.add_form.textEdit.toPlainText()
            state_id = self.add_form.comboBox_3.currentIndex()
            card_id = self.add_form.comboBox.currentIndex()
            term_end = self.add_form.dateEdit.date().toPyDate()
            term_end_str = term_end.strftime("%Y-%m-%d")
            duration_id = self.add_form.comboBox_2.currentIndex()
            price = self.add_form.textEdit_2.toPlainText()
            tuple_to_add = (service_name, state_id, card_id, duration_id, float(price), term_end_str)
            self.db_driver.add_subscription_to_db(tuple_to_add)
            self.table.setRowCount(self.table.rowCount() + 1)
            self.load_from_file()
            self.color_table()
            self.add_form.close()

    # сохранение изменений в БД
    def update_subscription(self):
        result_tuple = []
        result_tuple.append(self.t[0])
        result_tuple.append(self.edit_form.textEdit.toPlainText())
        result_tuple.append(self.edit_form.comboBox_3.currentIndex())
        result_tuple.append(self.edit_form.comboBox.currentIndex())
        result_tuple.append(self.edit_form.comboBox_2.currentIndex())
        result_tuple.append(self.edit_form.textEdit_2.toPlainText())
        res_date = self.edit_form.dateEdit.date().toPyDate()
        result_tuple.append(res_date.strftime("%Y-%m-%d"))
        self.db_driver.update_sub(result_tuple)
        self.load_from_file()
        self.color_table()
        self.edit_form.close()






