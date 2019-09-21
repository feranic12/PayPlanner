from PyQt5.QtWidgets import QWidget, QMessageBox
from widget_add import Ui_Form


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

    def save_new_subscription(self):pass

    def check_form(self):
        if self.textEdit.toPlainText() == "" or self.textEdit_2.toPlainText == "":
            msg = QMessageBox.setWindowTitle("Внимание!")
            msg.setText("Внимание! Заполнены не все поля!")
            msg.setStandardButtons(QMessageBox.OK)
            msg.exec_()




