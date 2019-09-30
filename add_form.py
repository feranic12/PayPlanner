from PyQt5.QtWidgets import QWidget, QMessageBox
import widget_add
from base_form import BaseForm


# класс, представляющий форму добавления новой записи, наследующий, в т.ч. от класса, полученного в визуальном редакторе
class AddForm(QWidget, widget_add.Ui_Form, BaseForm):
    def __init__(self, app):
        QWidget.__init__(self)
        self.app = app
        self.setupUi(self)
        self.pushButton.clicked.connect(self.save_new_subscription)
        self.advanced_setup()

    # сохранение новой записи в БД по кнопке "Сохранить"
    def save_new_subscription(self):
        if self.check_form():
            service_name = self.textEdit.toPlainText()
            state_id = self.comboBox_3.currentIndex()
            card_id = self.comboBox.currentIndex()
            term_end = self.dateEdit.date().toPyDate()
            term_end_str = term_end.strftime("%Y-%m-%d")
            duration_id = self.comboBox_2.currentIndex()
            price = self.textEdit_2.toPlainText()
            tuple_to_add = (service_name, state_id, card_id, duration_id, float(price), term_end_str)
            self.app.db_driver.add_subscription_to_db(tuple_to_add)
            self.app.table.setRowCount(self.app.table.rowCount() + 1)
            self.app.load_from_file()
            self.close()

    # проверка на заполненность обязательных полей
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






