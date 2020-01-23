from PyQt5.QtWidgets import QWidget, QMessageBox
from widget_add import Ui_Form
from base_form import BaseForm


# класс, представляющий форму добавления новой записи, наследующий, в т.ч. от класса, полученного в визуальном редакторе
class AddForm(QWidget, Ui_Form, BaseForm):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(app.save_new_subscription)
        self.advanced_setup(app)

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







