from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QDate
from widget_add import Ui_Form
from datetime import datetime
from base_form import BaseForm


class EditForm(QWidget, Ui_Form, BaseForm):
    def __init__(self, app):
        self.app = app
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Редактирование подписки")
        self.pushButton.clicked.connect(self.update_subscription)
        self.advanced_setup()

    def update_subscription(self):
        self.db_driver.update_sub()

