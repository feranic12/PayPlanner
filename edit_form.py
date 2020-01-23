from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QDate
import widget_add
from base_form import BaseForm


# класс, представляющий форму редактирования подписки, наследующий, в т.ч. от класса, полученного в визуальном редакторе
class EditForm(QWidget, widget_add.Ui_Form, BaseForm):
    def __init__(self, app, t):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setFixedSize(356, 277)
        self.setWindowTitle("Редактирование подписки")
        self.pushButton.clicked.connect(app.update_subscription)
        self.advanced_setup(app)
        self.textEdit.setText(t[1])
        self.comboBox_3.setCurrentIndex(t[2])
        self.comboBox.setCurrentIndex(t[3])
        self.comboBox_2.setCurrentIndex(t[4])
        self.textEdit_2.setText(str(t[5]))
        self.dateEdit.setDate(
            QDate(int(t[6][:4]), int(t[6][5:7]), int(t[6][8:10])))



