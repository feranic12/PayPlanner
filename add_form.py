from PyQt5.QtWidgets import QWidget, QMessageBox
from widget_add import Ui_Form
from datetime import datetime


class AddForm(QWidget, Ui_Form):
    def __init__(self, db_driver):
        self.db_driver = db_driver
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.save_new_subscription)
        durations = self.db_driver.get_all_durations()
        for d in durations:
            self.comboBox_2.addItem(d[1])
        bank_cards = self.db_driver.get_all_bank_cards()
        for bc in bank_cards:
            self.comboBox.addItem(bc[3]+' '+bc[1][-4:])

    def save_new_subscription(self):
        if self.check_form():
            service_name = self.textEdit.toPlainText()
            state_id = 0
            card_id = self.comboBox.currentIndex()
            term_end = self.dateEdit.date().toPyDate()
            term_end_str = term_end.strftime("%Y,%m,%d")
            duration_id = self.comboBox_2.currentIndex()
            price = self.textEdit_2.toPlainText()
            tuple_to_add = (service_name, state_id, card_id, term_end_str, duration_id, price)
            self.db_driver.add_subscription_to_db(tuple_to_add)

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




