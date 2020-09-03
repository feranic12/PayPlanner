from PyQt5.QtWidgets import QWidget, QMainWindow, QMessageBox
from PyQt5.QtCore import QDate
from widget_add import Ui_Form
from base_form import BaseForm


# класс, представляющий форму редактирования подписки, наследующий, в т.ч. от класса, полученного в визуальном редакторе
class EditForm(QWidget, Ui_Form, BaseForm):
    def __init__(self, app, sub):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setFixedSize(356, 277)
        self.setWindowTitle("Редактирование подписки")
        self.pushButton.clicked.connect(app.update_subscription)
        self.advanced_setup(app)
        self.textEdit.setText(sub[1])
        self.comboBox_3.setCurrentIndex(sub[2])
        self.comboBox_2.setCurrentIndex(sub[3])
        self.textEdit_2.setText(str(sub[4]))
        self.dateEdit.setDate(
            QDate(int(sub[5][:4]), int(sub[5][5:7]), int(sub[5][8:10])))



