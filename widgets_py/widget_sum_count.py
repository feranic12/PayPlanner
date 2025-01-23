from datetime import date, timedelta

from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox

from widgets_py.widget_sum_count_from_ui import Ui_Form


class SumCountForm(QWidget, Ui_Form):
    def __init__(self, app):
        QWidget.__init__(self)
        self.setupUi(self)
        self.Window = True
        self.dateEdit.setDate(date.today())
        self.dateEdit_2.setDate(date.today())
        self.pushButton.clicked.connect(app.show_sum_price)
