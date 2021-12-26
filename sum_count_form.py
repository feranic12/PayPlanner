from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox
from widget_sum_count import Ui_Form
from datetime import date, timedelta


class SumCountForm(QWidget, Ui_Form):
    def __init__(self, app):
        QWidget.__init__(self)
        self.setupUi(self)
        self.dateEdit.setDate(date.today())
        self.dateEdit_2.setDate(date.today())
        self.pushButton.clicked.connect(app.show_sum_price)