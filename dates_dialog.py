from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox
from widget_dates import Ui_Dialog


class DatesDialog(QDialog, Ui_Dialog):
    def __init__(self, app):
        QDialog.__init__(self)
        self.buttonBox.accepted.connect(app.calculate_sum_price)