from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QDate
from widget_add import Ui_Form
from base_form import BaseForm


# класс, представляющий форму редактирования подписки, наследующий, в т.ч. от класса, полученного в визуальном редакторе
class EditForm(QWidget, Ui_Form, BaseForm):
    def __init__(self, app, t):
        self.app = app
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Редактирование подписки")
        self.pushButton.clicked.connect(self.update_subscription)
        self.advanced_setup()
        self.t = t
        self.textEdit.setText(t[1])
        self.comboBox_3.setCurrentIndex(t[2])
        self.comboBox.setCurrentIndex(t[3])
        self.comboBox_2.setCurrentIndex(t[4])
        self.textEdit_2.setText(str(t[5]))
        self.dateEdit.setDate(
            QDate(int(t[6][:4]), int(t[6][5:7]), int(t[6][8:10])))

    # сохранение изменений в БД
    def update_subscription(self):
        t = self.t
        result_tuple = []
        result_tuple.append(t[0])
        result_tuple.append(self.textEdit.toPlainText())
        result_tuple.append(self.comboBox_3.currentIndex())
        result_tuple.append(self.comboBox.currentIndex())
        result_tuple.append(self.comboBox_2.currentIndex())
        result_tuple.append(self.textEdit_2.toPlainText())
        res_date = self.dateEdit.date().toPyDate()
        result_tuple.append(res_date.strftime("%Y-%m-%d"))
        self.app.db_driver.update_sub(result_tuple)
        self.app.load_from_file()
        self.close()

