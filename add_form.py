from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QDate
from widget_add import Ui_Form
from datetime import datetime
from base_form import BaseForm


class AddForm(QWidget, Ui_Form, BaseForm):
    def __init__(self, app):
        self.app = app
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.save_new_subscription)
        self.advanced_setup()

    def save_new_subscription(self):
        if self.check_form():
            service_name = self.textEdit.toPlainText()
            state_id = self.comboBox_3.currentIndex()
            card_id = self.comboBox.currentIndex()
            term_end = self.dateEdit.date().toPyDate()
            term_end_str = term_end.strftime("%Y,%m,%d")
            duration_id = self.comboBox_2.currentIndex()
            price = self.textEdit_2.toPlainText()
            tuple_to_add = (service_name, state_id, card_id, duration_id, price, term_end_str)
            self.app.db_driver.add_subscription_to_db(tuple_to_add)
            self.app.table.setRowCount(self.app.table.rowCount() + 1)
            self.app.load_from_file()
            self.clear()
            self.close()

    def check_form(self):
        if self.textEdit.toPlainText() == "" or self.textEdit_2.toPlainText() == "":
            msg = QMessageBox()
            msg.setWindowTitle("Внимание!")
            msg.setText("Внимание! Заполнены не все поля!")
            msg.addButton("OK", QMessageBox.AcceptRole)
            msg.exec()
            return False
        else:
            return True

    def clear(self):
        self.textEdit.clear()
        self.textEdit_2.clear()
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.dateEdit.setDate(QDate(2020, 1, 1))






