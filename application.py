import sys
from time import strptime, mktime, sleep
from datetime import datetime, date, timedelta

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, \
    QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QMessageBox
from PyQt5.QtCore import QSize, Qt, QDate
from PyQt5 import QtGui
from plyer import notification

import db
import util
import exceptions
from widgets_py.widget_add import AddForm
from widgets_py.widget_edit import EditForm
from widgets_py.widget_sum_count import SumCountForm
from widgets_py.widget_matplotlib import MplWidget


# класс приложения, представляющий главное окно приложения
class MyApp(QMainWindow):
    # инициализация элементов главного окна
    def __init__(self):
        super().__init__()
        self.db_driver = db.DB("pay_planner_db.db")

        self.setFixedSize(QSize(950, 450))
        self.setWindowTitle("Подписчик")
        self.central_widget = QWidget()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        headers = ["Название сервиса", "Состояние подписки",
                   "Период продления", "Сумма", "Срок окончания"]
        self.table.setRowCount(self.db_driver.get_subs_count())
        self.table.setHorizontalHeaderLabels(headers)
        for x in range(self.table.columnCount()):
            self.table.horizontalHeaderItem(x).setTextAlignment(Qt.AlignCenter)
            self.table.horizontalHeaderItem(x).setFont(
                QtGui.QFont("Times", 8, QtGui.QFont.Bold))
            self.table.setColumnWidth(x, 175)
        self.setCentralWidget(self.central_widget)

        self.button1 = QPushButton()
        self.button1.setText("Добавить")
        self.button2 = QPushButton()
        self.button2.setText("Редактировать")
        self.button3 = QPushButton()
        self.button3.setText("Удалить")
        self.button4 = QPushButton()
        self.button4.setText("Проверить")
        self.button5 = QPushButton()
        self.button5.setText("Сумма за период")
        self.button6 = QPushButton()
        self.button6.setText("Диаграмма")

        self.button1.clicked.connect(self.add_new_subscription)
        self.button2.clicked.connect(self.edit_selected)
        self.button3.clicked.connect(self.delete_subscription)
        self.button4.clicked.connect(self.check_updates)
        self.button5.clicked.connect(self.open_sum_count_form)
        self.button6.clicked.connect(self.show_diagram)
        self.table.doubleClicked.connect(self.edit_selected)

        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)
        hbox.addWidget(self.button3)
        hbox.addWidget(self.button4)
        vbox.addLayout(hbox)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.button5)
        hbox1.addWidget(self.button6)
        vbox.addLayout(hbox1)
        self.central_widget.setLayout(vbox)

        self.add_form = None
        self.edit_form = None
        self.sum_count_form = None
        self.mpl_widget = None

        self.check_updates()
        self.load_from_db()
        self.color_table()

    # покраска строк таблицы
    def color_table(self):
        subs = self.db_driver.get_all_subscriptions()
        for row in range(self.table.rowCount()):
            state = subs[row][2]
            color = None
            if state in (0, 1):
                color = "lightgreen"
            elif state == 2:
                color = "red"
            for col in range(self.table.columnCount()):
                cellinfo = QTableWidgetItem(self.table.item(row, col))
                cellinfo.setBackground(QtGui.QColor(color))
                self.table.setItem(row, col, cellinfo)

    # проверка необходимости продления каких-либо подписок
    # если истекают сегодня или завтра
    # и фактическое продление подписок, истекающих сегодня.
    def check_updates(self):
        subs = self.db_driver.get_all_subscriptions()
        # n - число подписок, оканчивающихся сегодня или завтра
        n = 0
        for sub in subs:
            # если подписка не прервана
            if sub[2] != 2:
                date_from = datetime.strptime(sub[5], "%Y-%m-%d").date()
                if date_from <= date.today() + timedelta(1):
                    n = n + 1
                    self.send_notification(sub)
                    sleep(5)
                # увеличение даты окончания периода подписки
                # на период действия подписки
                while date_from <= date.today():
                    # продление подписки
                    duration = self.db_driver.get_duration_by_id(sub[3])
                    date_from = util.date_forward(date_from, duration)
                self.db_driver.update_end_date(sub[0], date_from)

        # если были подписки, оканчивающиеся сегодняи или завтра,
        # перезагрузить таблицу
        if n > 0:
            self.load_from_db()
            self.color_table()
        else:
            msg_box = QMessageBox()
            msg_box.setText(
                "Подписок, подлежащих продлению, в данный момент нет.")
            msg_box.exec()

    # отправка push уведомления в трей Windows о том,
    # что скоро оканчивается срок подписки
    def send_notification(self, sub):
        # если подписка не прервана
        if sub[2] != 2:
            notification.notify(
                title='ПОДПИСЧИК',
                message=sub[5] + ' истекает срок продления подписки ' + sub[1]
                               + ' . Будет списано ' + str(sub[4]) + ' рублей',
                app_name='PayPlanner',
                app_icon='icons/icon1.ico'
            )

    # заполнение таблицы актуальными данными из БД
    def load_from_db(self):
        self.table.clearContents()
        subs_for_table = self.db_driver.get_subs_for_table()
        for row in range(subs_for_table.__len__()):
            for col in range(self.table.columnCount()):
                if col == 2:
                    cellinfo = QTableWidgetItem(
                        str(subs_for_table[row][col]) + " мес.")
                else:
                    cellinfo = QTableWidgetItem(str(subs_for_table[row][col]))
                self.table.setItem(row, col, cellinfo)

    # вызов формы добавления записи в таблицу
    def add_new_subscription(self):
        self.add_form = AddForm(self)
        self.add_form.show()

    # вызов формы редактирования записи табицы
    def edit_selected(self):
        subs = self.db_driver.get_all_subscriptions()
        row_num = self.table.currentRow()
        sub = subs[row_num]
        self.edit_form = EditForm(self, sub)
        self.edit_form.show()

    # вызов формы расчета суммы платежей по подпискам
    def open_sum_count_form(self):
        self.sum_count_form = SumCountForm(self)
        self.sum_count_form.show()

    # вывод результата расчета суммы платежей за выбранный период
    def show_sum_price(self):
        start_date = self.sum_count_form.dateEdit.date()
        end_date = self.sum_count_form.dateEdit_2.date()
        try:
            result_sum = self.calculate_sum_price(start_date, end_date)
        except exceptions.WrongDatesError:
            msg_box = QMessageBox()
            msg_box.setText("Ошибка! Дата начала позже даты окончания!")
            msg_box.exec()
            return
        msg_box = QMessageBox()
        msg_box.setText(
            "Сумма платежей за выбранный период: {0} рублей.".format(
                result_sum))
        msg_box.exec()

    # удаление выбранной записи из таблицы
    def delete_subscription(self):
        row_num = self.table.currentRow()
        id = self.db_driver.get_all_subscriptions()[row_num][0]
        self.db_driver.delete_sub(id)
        self.table.setRowCount(self.table.rowCount() - 1)
        self.load_from_db()
        self.color_table()

    # сохранение новой записи в БД по кнопке "Сохранить"
    def save_new_subscription(self):
        try:
            self.add_form.check_form()
        except exceptions.AddFormNotFilledError:
            msg = QMessageBox()
            msg.setWindowTitle("Внимание!")
            msg.setText("Внимание! Заполнены не все поля!")
            msg.addButton("OK", QMessageBox.AcceptRole)
            msg.exec()
            return
        service_name = self.add_form.textEdit.toPlainText()
        state_id = self.add_form.comboBox_3.currentIndex()
        term_end = self.add_form.dateEdit.date().toPyDate()
        term_end_str = term_end.strftime("%Y-%m-%d")
        duration_id = self.add_form.comboBox_2.currentIndex()
        price = self.add_form.textEdit_2.toPlainText()
        tuple_to_add = (
            service_name, state_id, duration_id, float(price), term_end_str)
        self.db_driver.add_subscription_to_db(tuple_to_add)
        self.table.setRowCount(self.table.rowCount() + 1)
        self.load_from_db()
        self.color_table()
        self.add_form.close()

    # сохранение изменений в БД при редактировании какой-то записи
    def update_subscription(self, id):
        subs = self.db_driver.get_all_subscriptions()
        row_num = self.table.currentRow()
        sub = subs[row_num]
        result_tuple = []
        result_tuple.append(sub[0])
        result_tuple.append(self.edit_form.textEdit.toPlainText())
        result_tuple.append(self.edit_form.comboBox_3.currentIndex())
        result_tuple.append(self.edit_form.comboBox_2.currentIndex())
        result_tuple.append(self.edit_form.textEdit_2.toPlainText())
        res_date = self.edit_form.dateEdit.date().toPyDate()
        result_tuple.append(res_date.strftime("%Y-%m-%d"))
        self.db_driver.update_sub(result_tuple)
        self.load_from_db()
        self.color_table()
        self.edit_form.close()

    # подсчет суммарной стоимости подписок за период
    def calculate_sum_price(self, start_date, end_date):
        if start_date > end_date:
            raise exceptions.WrongDatesError
        result_sum = 0
        subs = self.db_driver.get_all_subscriptions()
        for sub in subs:
            date_from = datetime.strptime(sub[5], "%Y-%m-%d").date()
            duration = self.db_driver.get_duration_by_id(sub[3])
            # пока следующая дата меньше стартовой,
            # "холостой" прогон, пока дата не сравняется со стартовой
            while date_from < start_date:
                date_from = util.date_forward(date_from, duration)
            # начиная со стартовой даты, не просто прогоняем вперед дату,
            # но и увеличиваем итоговую сумму.
            while date_from <= end_date:
                if sub[2] != 2:
                    result_sum += sub[4]
                date_from = util.date_forward(date_from, duration)
        return result_sum

    # формирование набора данных для диаграммы на год вперёд,
    # начиная с месяца, следующего за текущим.
    def make_dataset(self):
        months = {1: "янв.", 2: "фев.", 3: "мар.", 4: "апр.",
                  5: "май", 6: "июн.", 7: "июл.", 8: "авг.",
                  9: "сен.", 10: "окт.", 11: "ноя.", 12: "дек."}
        sum_values = []
        xticks = []
        start_month = 1 \
            if datetime.today().month == 12 \
            else datetime.today().month + 1
        start_year = datetime.today().year + 1 \
            if datetime.today().month == 12 \
            else datetime.today().year
        for current_month in range(start_month, start_month + 12):
            if current_month <= 12:
                sum_values.append(
                    self.calculate_sum_price_for_one_month(
                        current_month, start_year))
                xticks.append(months[current_month] + str(start_year))
            else:
                sum_values.append(
                    self.calculate_sum_price_for_one_month(
                        current_month - 12, start_year + 1))
                xticks.append(
                    months[current_month - 12] + str(start_year + 1))
        dataset = [sum_values, xticks]
        return dataset

    # подсчет суммарной стоимости подписок за один месяц.
    # Результат будет использован для
    # построения столбчатой диаграммы за последующий год.
    def calculate_sum_price_for_one_month(self, month, year):
        start_date = date(year, month, 1)
        end_date = date(year, month, util.get_last_day_of_month(month, year))
        return self.calculate_sum_price(start_date, end_date)

    # вывод формы со столбчатой диаграммой на основе dataset
    def show_diagram(self):
        self.mpl_widget = MplWidget(self)
        self.mpl_widget.show()
